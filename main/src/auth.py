import os
import re

from flask import Blueprint, redirect, url_for, request, flash
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db, profile_pictures, default_render_template
from .models import Users, get_user_by_id_or_name, role_required

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=["GET", "POST"])
def route_register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not re.fullmatch(r"[a-zA-Z]+[\w]*", username):
            flash('Not a valid username!', 'error')
            return default_render_template("sign_up.html")
        if not 2 < len(username) < 31:
            flash('Username has an invalid length!', 'error')
            return default_render_template("sign_up.html")

        if Users.query.filter_by(username=username).first():
            flash('Username already taken!', 'error')
            return default_render_template("sign_up.html")

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        new_user = Users(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.route_login"))

    return default_render_template("sign_up.html")

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
            flash('Invalid username or password', 'error')
            return default_render_template("login.html")

    return default_render_template("login.html")

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
        profile_pictures.save(request.files["pfp"], name=current_user.id)
    return redirect('/')

@auth.route("/settings", methods=["GET", "POST"])
@login_required
def route_settings():
    if request.method == 'POST':
        if "name" in request.form:
            username = request.form.get('name')
            if not re.fullmatch(r"[a-zA-Z]+[\w]*", username):
                flash('Not a valid username!', 'error')
            elif not 2 < len(username) < 31:
                flash('Username has an invalid length!', 'error')
            elif Users.query.filter_by(username=username).first():
                flash('Username already taken!', 'error')
            else:
                change_account_name(current_user.username, username)
        if "pfp" in request.files:
            if os.path.exists('uploads/profile_pictures/' + str(current_user.id)):
                os.remove('uploads/profile_pictures/' + str(current_user.id))
            profile_pictures.save(request.files["pfp"], name=str(current_user.id))

    return default_render_template('settings.html')

@auth.route("/userlist")
@login_required
@role_required('admin')
def route_list_users():
    page = request.args.get('page')
    length = request.args.get('page_length')
    page = int(page) if page and page.isdigit() else 0
    length = int(length) if length and length.isdigit() else 10
    usercount = len(Users.query.all())
    users = Users.query.all()[page*length:page*length+length] if length > 0 and page*length < usercount else Users.query.all()[0:10]
    next_page = ('/userlist?page=' + str(page+1) + (('&page_length=' + str(length)) if length != 10 else '')) if (page+1)*length < usercount else None
    previous_page = ('/userlist?page=' + str(page-1) + (('&page_length=' + str(length)) if length != 10 else '')) if page-1 >= 0 else None
    return default_render_template('moderation/userlist.html', users=users, next=next_page, previous=previous_page)

@auth.route("/moderation/user/<user>")
@login_required
@role_required('admin')
def route_admin_actions(user):
    if not get_user_by_id_or_name(user):
        flash('User not found!', 'error')
        return redirect('/userlist')
    return default_render_template('moderation/userpage.html', moderated_user=get_user_by_id_or_name(user))

@auth.route("/delete_account/<account>")
@login_required
@role_required('admin')
def route_delete_user_account(account):
    if delete_account(account):
        flash('Deletion Successful!', 'info')
    else:
        flash('A problem occurred when trying to delete user ' + account + '.', 'error')
    return redirect('/userlist', code=302)

def delete_account(account):
    user = get_user_by_id_or_name(account)
    if not user:
        return False
    db.session.delete(user)
    db.session.commit()
    if os.path.exists('uploads/profile_pictures/' + str(user.id)):
        os.remove('uploads/profile_pictures/' + str(user.id))
    return True

def change_account_name(account, new_name):
    user = get_user_by_id_or_name(account)
    if not user:
        return False
    user.username = new_name
    db.session.commit()
    return True