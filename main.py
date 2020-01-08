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
    print(session)
    print(session.get('HL_USER'))
    if session.get('HL_USER'):
        username = session.get('HL_USER')
        user_profile = dbase.select_user(username)[0]
    else:
       user_profile = (0,"","","Guest","Profile",0,"","")
    return render_template('profile.html', user=user_profile)

def isBlank (myString):
    if myString and myString.strip():
        return False
    return True

if __name__ == '__main__':
    main.run(debug=True)