import os.path
import re
import secrets
from datetime import timedelta
from functools import wraps

from flask import Flask, request, render_template, redirect, url_for, send_file, send_from_directory, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES  # do 'pip install flask-reuploaded' instead of using the deprecated 'flask-uploads'
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOADED_PHOTOS_DEST"] = "uploads/profile_pictures"
app.config["SECRET_KEY"] = str(secrets.SystemRandom().getrandbits(128))

# Session configuration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

profile_pictures = UploadSet("photos", IMAGES)
configure_uploads(app, profile_pictures)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    role = db.Column(db.String(20), default='user')

    def has_role(self, role):
        return self.role == role

    def is_admin(self):
        return self.role == 'admin'

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_role(role):
                flash('Access denied. Insufficient permissions.')
                return redirect(url_for('route_index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
def route_index():
    return render_template("home.html", user=current_user)

@app.route('/main.css')
def route_style():
    return send_file('style/main.css')

@app.route('/register', methods=["GET", "POST"])
def route_register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not re.fullmatch(r"[a-zA-Z]+[\w]*", username):
            return render_template("sign_up.html", error="Not a valid username!")
        if not 2 < len(username) < 31:
            return render_template("sign_up.html", error="Username has an invalid length!")

        if Users.query.filter_by(username=username).first():
            return render_template("sign_up.html", error="Username already taken!")

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        new_user = Users(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("sign_up.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("route_index"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route("/logout")
@login_required
def route_logout():
    logout_user()
    return redirect(url_for("route_index"))

@app.route("/delete_account")
@login_required
def route_delete_account():
    delete_account(current_user.username)
    logout_user()
    return redirect(url_for("route_index"))

def delete_account(account):
    user = Users.query.filter_by(username=account).first()
    db.session.delete(user)
    db.session.commit()
    if os.path.exists('uploads/profile_pictures/' + account):
        os.remove('uploads/profile_pictures/' + account)

def change_account_name(account, new_name):
    user = Users.query.filter_by(username=account).first()
    user.username = new_name
    db.session.commit()
    if os.path.exists('uploads/profile_pictures/' + account):
        os.rename('uploads/profile_pictures/' + account, 'uploads/profile_pictures/' + new_name)

@app.route("/upload_profile_picture", methods=["POST"])
@login_required
def upload_pfp():
    if "pfp" in request.files:
        profile_pictures.save(request.files["pfp"], name=current_user.username)
    return redirect(url_for("route_index"))

@app.route("/profile/picture/<profile>")
def route_pfp(profile):
    return send_from_directory('uploads/profile_pictures/', profile)\
        if os.path.exists('uploads/profile_pictures/' + profile)\
        else send_file('static/empty_pfp.svg')

@app.route("/profile/picture/me")
@login_required
def route_pfp_me():
    return redirect('/profile/picture/' + current_user.username, code=301)

@app.route("/settings", methods=["GET", "POST"])
@login_required
def route_settings():
    if request.method == 'POST':
        errors = []
        if "name" in request.form:
            username = request.form.get('name')
            if not re.fullmatch(r"[a-zA-Z]+[\w]*", username):
                errors.append("Not a valid username!")
            elif not 2 < len(username) < 31:
                errors.append("Username has an invalid length!")
            elif Users.query.filter_by(username=username).first():
                errors.append("Username already taken!")
            else:
                change_account_name(current_user.username, username)
        if "pfp" in request.files:
            profile_pictures.save(request.files["pfp"], name=current_user.username)

        # return with errors if errors occurred
        if len(errors) > 0:
            return render_template('settings.html', user=current_user, errors=errors)
    return render_template('settings.html', user=current_user)

@app.route("/js/<script>")
def route_script(script):
    return send_from_directory('script/', script)

if __name__ == "__main__":
    app.run(debug=True)