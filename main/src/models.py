from functools import wraps

from flask import flash, redirect
from flask_login import UserMixin, current_user

from .extensions import db

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
                return redirect('/')
            return f(*args, **kwargs)
        return decorated_function
    return decorator