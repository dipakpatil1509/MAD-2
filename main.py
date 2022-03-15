from datetime import timedelta
import os
from flask import Flask, jsonify, redirect, session, url_for, flash
from flask_restful import Api
from flask_security import SQLAlchemySessionUserDatastore, Security
from sqlalchemy import exc
from application.database import db
from flask_login import LoginManager
from flask_migrate import Migrate
from application.error import APIException
from flask_cors import CORS

from application.models.user_mode import Role, User

app = None
api = None

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    SQLITE_DB = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_FRESHNESS_GRACE_PERIOD = timedelta(days=30)
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Auth-Token"
    SECURITY_LOGIN_URL = "/api/login"
    SECURITY_REGISTER_URL = "/api/register"
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    WTF_CSRF_ENABLED = False


class LocalDevelopment(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="")
    app.logger.debug("Starting Server")
    app.config.from_object(LocalDevelopment)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SECRET_KEY'] = '21f1004451abcd.'
    app.config['SECURITY_PASSWORD_SALT'] = "21f100##4451@$"
    db.init_app(app)
    

    app.app_context().push()
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)
    api = Api(app)
    CORS(app)
    return app, api


app, api = create_app()

migrate = Migrate(app, db, render_as_batch=True)


from application.api.home import Home
api.add_resource(Home, '/api/decks', methods=['GET'])

from application.api.profile import UserAPI
api.add_resource(UserAPI, "/api/user")

from application.api.auth import Logout
api.add_resource(Logout, "/api/logout")

from application.api.deck import DeckAPI
api.add_resource(DeckAPI, '/api/deck', '/api/deck/<int:deck_id>', methods=['GET', 'POST', 'PUT', "DELETE"])

from application.api.card import CardAPI
api.add_resource(CardAPI, '/api/card', '/api/card/<int:card_id>', methods=['GET', 'POST', 'PUT', "DELETE"])

from application.api.review import ReviewAPI
api.add_resource(ReviewAPI, '/api/review', '/api/review/<int:response_id>', methods=['GET', 'POST', 'PUT', "DELETE"])

if __name__ == "__main__":
    db.create_all()
    app.run()
