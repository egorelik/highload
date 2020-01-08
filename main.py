from flask import Flask, render_template, request, Blueprint, session, redirect, url_for
from flask_login import login_required, current_user
from . import dbase
import os

template_dir = os.path.dirname(".")
template_dir = os.path.join(template_dir, 'templates')
main = Blueprint('main',__name__, template_folder=template_dir)

@main.route("/", methods=['POST','GET'])
def index():
    return redirect(url_for('main.profile'))

@main.route("/profile", methods=['POST','GET'])
def profile():
    if session.get('HL_USER'):
        username = session.get('HL_USER')
        user = dbase.select_user(username)
        user_profile = user[0]
        user_id = (user[0][0],)
        interests_list = dbase.select_user_interest(user_id)
    else:
       user_profile = (0,"","","Guest","Profile",0,"","")
       interests_list = ()
    return render_template('profile.html', user=user_profile, interests=interests_list)

def isBlank (myString):
    if myString and myString.strip():
        return False
    return True

