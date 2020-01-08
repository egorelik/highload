from flask import Flask
from flask_login import LoginManager
from db.social import SocialDB
import os
import sys

cur_dir = os.path.dirname(".")
db_dir = os.path.join(cur_dir, 'templates')
sys.path.insert(0, db_dir)

dbase = SocialDB()

def create_app():
    app = Flask(__name__)
    app.config['MYSQL_HOST'] = ''
    app.config['MYSQL_DB'] = ''
    app.config['MYSQL_USER'] = ''
    app.config['MYSQL_PASSWORD'] = ''
    app.config['SECRET_KEY'] = ''

    dbase.init(app.config)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
