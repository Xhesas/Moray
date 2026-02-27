from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES

db = SQLAlchemy()
login_manager = LoginManager()
profile_pictures = UploadSet("photos", IMAGES)