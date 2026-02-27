import os
import re

from flask import Blueprint, redirect, url_for, request, render_template
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db, profile_pictures
from .models import Users

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=["GET", "POST"])
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

        return redirect(url_for("auth.route_login"))

    return render_template("sign_up.html")

@auth.route("/login", methods=["GET", "POST"])
def route_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect('/')
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@auth.route("/logout")
@login_required
def route_logout():
    logout_user()
    return redirect('/')

@auth.route("/delete_account")
@login_required
def route_delete_account():
    delete_account(current_user.username)
    logout_user()
    return redirect('/')

@auth.route("/upload_profile_picture", methods=["POST"])
@login_required
def upload_pfp():
    if "pfp" in request.files:
        profile_pictures.save(request.files["pfp"], name=current_user.username)
    return redirect('/')

@auth.route("/settings", methods=["GET", "POST"])
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
            if os.path.exists('uploads/profile_pictures/' + current_user.username):
                os.remove('uploads/profile_pictures/' + current_user.username)
            profile_pictures.save(request.files["pfp"], name=current_user.username)

        # return with errors if errors occurred
        if len(errors) > 0:
            return render_template('settings.html', user=current_user, errors=errors)
    return render_template('settings.html', user=current_user)

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