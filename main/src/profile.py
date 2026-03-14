import os

from flask import Blueprint, abort, redirect, send_file, send_from_directory
from flask_login import login_required, current_user

from main.src.extensions import default_render_template
from main.src.models import get_user_by_id_or_name

profile_app = Blueprint('profile', __name__)

@profile_app.route('/profile/<profile>')
def route_profile(profile):
    profile = get_user_by_id_or_name(profile)
    if not profile:
        abort(404)
    return default_render_template('profile.html', profile=profile)

@profile_app.route('/profile/me')
@login_required
def route_me():
    return redirect('/profile/' + current_user.username, code=301)

@profile_app.route("/profile/<profile>/picture")
def route_pfp(profile):
    user = get_user_by_id_or_name(profile)
    return send_from_directory('uploads/profile_pictures/', str(user.id)) \
        if os.path.exists('uploads/profile_pictures/' + str(user.id)) \
        else send_file('static/resources/empty_pfp.svg')

@profile_app.route("/profile/me/picture")
@login_required
def route_pfp_me():
    return redirect('/profile/' + current_user.username + '/picture', code=301)