# this file is going to make website
# folder as python package

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# os means operating system
from os import path
# login manager is going help us manage all the logging in related things
from flask_login import LoginManager


# creating database object
# this is the object we are going to use whenever
# we want to add, create, delete whatever
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    # this secret key is needed to keep client-side
    # sessions secure
    app.config["SECRET_KEY"] = "TOSHA IS ATTACKING"

    # here I am telling to flask that my database is located
    # at this location DB_NAME
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"

    # initializing database by giving it to our flask
    db.init_app(app)

    # register blueprints in init.py
    # blueprints contain some views or
    # urls for our application
    # and here they are
    from .views import views
    from .auth import auth

    # register blueprints in init.py
    # url_prefix is saying all of urls
    # that stored inside of these blueprints
    # file how do I access them
    # prefix "/" means no prefix
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # importing database models from module "models.py"
    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    # where user need to go if user is not logged in
    login_manager.login_view = 'auth.login'
    # telling login manager which app we are using
    login_manager.init_app(app)

    # telling flask how we load a user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


# checking if the database already exists and
# if it does not it is going to create this db
def create_database(app):
    # here I use path module for checking if the
    # database exists, or it does not
    if not path.exists("website/" + DB_NAME):
        # db.create_all(app=app)
        # print("Created Database!")
        with app.app_context():
            db.create_all()
            print("Created Database!")
