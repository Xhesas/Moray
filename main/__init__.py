import argparse
import secrets
from datetime import timedelta

from flask import Flask, render_template, make_response
from flask_uploads import configure_uploads  # do 'pip install flask-reuploaded' instead of using the deprecated 'flask-uploads'
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.proxy_fix import ProxyFix

from main.src.extensions import db, login_manager, profile_pictures

def create_app():
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

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.route_login"

    configure_uploads(app, profile_pictures)

    from main.src.models import Users
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        code = e if type(e) == int else e.code
        return make_response(render_template('exception.html', code=code), code)

    from main.src.auth import auth
    app.register_blueprint(auth)

    from main.src.static import static
    app.register_blueprint(static)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--Debug", action="store_true", help="Activate debug mode")
    args = parser.parse_args()
    app = create_app()
    # set proper wsgi for app if not debug
    if not args.Debug:
        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
        )
    app.run(debug=args.Debug)