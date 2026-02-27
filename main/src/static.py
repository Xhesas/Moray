import os

from flask import Blueprint, render_template, send_file, send_from_directory, redirect, abort
from flask_login import current_user, login_required

static = Blueprint('static', __name__)

@static.route('/')
def route_index():
    return render_template("home.html", user=current_user)

@static.route('/main.css')
def route_style():
    return send_file('static/style/main.css')

@static.route("/profile/picture/<profile>")
def route_pfp(profile):
    return send_from_directory('uploads/profile_pictures/', profile) \
        if os.path.exists('uploads/profile_pictures/' + profile) \
        else send_file('static/resources/empty_pfp.svg')

@static.route("/profile/picture/me")
@login_required
def route_pfp_me():
    return redirect('/profile/picture/' + current_user.username, code=301)

@static.route("/js/<script>")
def route_script(script):
    return send_from_directory('static/script/', script)

@static.route("/resources/<resource>")
def route_resources(resource):
    return send_from_directory('static/resources/', resource)

@static.route("/favicon.ico")
def route_favicon():
    return send_file('static/resources/favicon.ico')

@static.route("/contact")
def route_contact():
    return render_template('contact.html', user=current_user)

@static.route("/info/<info>")
def route_info(info):
    match info:
        case "data":
            return render_template('info.html', info="Data Policy", content=[
                {'type': 'h2', 'text': 'Data collected from serving requests'},
                {'type': 'p' , 'text': 'Data collected from serving requests including request path, header, resulting http code, time of request and ip address are stored for '
                                       'the purpose of keeping server integrity, preventing malicious behavior and moderating visits. All of the produced information is kept '
                                       'secure and only accessible to the server owners.'},
                {'type': 'br', 'text': ''},
                {'type': 'h2', 'text': 'Account data'},
                {'type': 'p' , 'text': 'Data produced from account activities are stored securely and are only accessible to server owners and moderation. Passwords are always '
                                       'stored encrypted. Data uploaded by a user like profile pictures or other profile information are available to all other users.'},
                {'type': 'br', 'text': ''},
                {'type': 'h2', 'text': 'Data collected from forms and other methods of posting'},
                {'type': 'p' , 'text': 'Data resulting from proactive posts like forms may be stored on the server along with request path, header, time of request, ip address '
                                       'and client information and are only accessible to server owners.'}
            ])
        case "cookies":
            return render_template('info.html', info="Cookies Policy", content=[
                {'type': 'h2', 'text': 'Cookie usage'},
                {'type': 'p' , 'text': 'Cookies are only used for essential functionalities such as session management as part of authentication. All cookies are strictly '
                                       'https only and non cross origin.'},
                {'type': 'br', 'text': ''},
                {'type': 'h2', 'text': 'Cookie creation'},
                {'type': 'p' , 'text': 'Cookies are only created and set when a user enters a session i.e. signs in with an account.'}
            ])
    abort(404)