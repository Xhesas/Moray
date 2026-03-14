import argparse
import secrets
from datetime import timedelta
from os import chdir
from os.path import dirname, abspath

from flask import Flask, make_response
from flask_migrate import upgrade, init, migrate, downgrade
from flask_uploads import configure_uploads  # do 'pip install flask-reuploaded' instead of using the deprecated 'flask-uploads'
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.proxy_fix import ProxyFix

from main.src.extensions import db, login_manager, profile_pictures, langs, default_render_template, migrate as migrate_db

chdir(dirname(abspath(__file__)))

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
    migrate_db.init_app(app, db)
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
        return make_response(default_render_template('exception.html', code=code), code)

    from main.src.auth import auth
    app.register_blueprint(auth)

    from main.src.static import static
    app.register_blueprint(static)

    from main.src.lang import lang_app
    app.register_blueprint(lang_app)

    from main.src.profile import profile_app
    app.register_blueprint(profile_app)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--Debug", action="store_true", help="Activate debug mode")
    parser.add_argument("-i", "--Initiate", action="store_true", help="Initiate database")
    parser.add_argument("-p", "--Prepare", action="store_true", help="Prepare database")
    parser.add_argument("-u", "--Upgrade", action="store_true", help="Upgrade database")
    parser.add_argument("-dg", "--Downgrade", action="store_true", help="Downgrade database")
    args = parser.parse_args()
    app = create_app()
    # set proper wsgi for app if not debug
    if not args.Debug:
        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
        )
    if args.Initiate:
        with app.app_context():
            print('initiate database upgrade...')
            init()
        exit(0)
    if args.Prepare:
        with app.app_context():
            print('preparing upgrade...')
            migrate()
        exit(0)
    if args.Upgrade:
        with app.app_context():
            print('upgrading database...')
            upgrade()
        exit(0)
    if args.Downgrade:
        with app.app_context():
            print('Downgrading database...')
            downgrade()
        exit(0)
    app.run(debug=args.Debug)