from flask import render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES

from main.src.langs import Lang

db = SQLAlchemy()
login_manager = LoginManager()
profile_pictures = UploadSet("photos", IMAGES)

from main.src.langs.german import German

langs = {
    'deu': German(),
    'lvk': Lang('lvk')
}

def default_render_template(*args, **kwargs):
    return render_template(*args, **kwargs, langs=langs)