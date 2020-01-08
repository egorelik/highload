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

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return dbase.select_user(int(user_id))

    return app
