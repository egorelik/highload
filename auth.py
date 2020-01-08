from flask import Flask, render_template, request, Blueprint, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from . import dbase
import os

template_dir = os.path.dirname(".")
template_dir = os.path.join(template_dir, 'templates')
auth = Blueprint('auth',__name__, template_folder=template_dir)

@auth.route("/registration", methods=['POST','GET'])
def registration():
    username = request.form.get('username')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    city = request.form.get('city')
    country = request.form.get('country')
    interests = request.form.getlist('interests')
    age = 0 if isBlank(request.form.get('age')) else int(request.form.get('age'))

    print("%s | %s | %s | %s | %s | %s | %d | %s" % (username, password, first_name, last_name, city, country, age, interests))

    if not isBlank(username):
        user = dbase.select_user(username)
        if user:
           return redirect(url_for('auth.login'))

    user_interests = dbase.select_interests();
    if isBlank(username) \
        or isBlank(password) \
        or isBlank(first_name) \
        or isBlank(last_name) \
        or isBlank(city) \
        or isBlank(country):
        return render_template("registration.html", interests_list=user_interests)

    password = generate_password_hash(password, method='sha256')
    user = (username,password,first_name,last_name,age,city,country)
    dbase.add_new_user(user)
    user_id = dbase.select_user(username)[0][0]
    for interest in interests:
        print(user_id)
        print(interest)
        dbase.add_user_interest((user_id,interest))

    return redirect(url_for('auth.login'))

@auth.route("/login", methods=['POST','GET'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if isBlank(username) \
        or isBlank(password):
        return render_template("login.html")

    if not is_loggedin(username):
        user = dbase.select_user(username)[0]
        user_password = user[2]
        if not user or not check_password_hash(user_password, password):
            return redirect(url_for('auth.login'))

        session['HL_USER'] = user[1]
    print(session)
    return redirect(url_for('main.profile'))

@auth.route("/logout", methods=['POST','GET'])
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def isBlank(myString):
    if myString and myString.strip():
        return False
    return True

def is_loggedin(username):
    if isBlank(session.get('HL_USER')):
        return False
    else:
        return True
