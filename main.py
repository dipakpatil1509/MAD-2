from datetime import datetime, timedelta
import os
from flask import Flask, render_template
from flask_restful import Api, marshal
from flask_security import SQLAlchemySessionUserDatastore, Security
from application.database import db
from application import workers
from flask_migrate import Migrate
from flask_cors import CORS
from jinja2 import Template
from application.models.user_mode import Role, User
from flask_weasyprint import render_pdf, HTML

app = celery= None
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
    CELERY_ENABLE_UTC = False
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    REDIS_URL = "redis://localhost:6379"


class LocalDevelopment(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    REDIS_URL = "redis://localhost:6379"


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

    
    celery = workers.celery
    
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"],
    )

    celery.Task = workers.ContextTask

    return app, api, celery


app, api, celery = create_app()

migrate = Migrate(app, db, render_as_batch=True)


from application.api.home import Home
api.add_resource(Home, '/api/decks', methods=['GET'])

from application.api.profile import UserAPI
api.add_resource(UserAPI, "/api/user")

from application.api.profile import WebhooksAPI
api.add_resource(WebhooksAPI, '/api/user/webhooks', methods=['GET', 'POST'])

from application.api.auth import Logout
api.add_resource(Logout, "/api/logout")

from application.api.auth import WelcomeEmail
api.add_resource(WelcomeEmail, "/api/welcome")

from application.api.deck import DeckAPI
api.add_resource(DeckAPI, '/api/deck', '/api/deck/<int:deck_id>', methods=['GET', 'POST', 'PUT', "DELETE"])

from application.api.card import CardAPI
api.add_resource(CardAPI, '/api/card', '/api/card/<int:card_id>', methods=['GET', 'POST', 'PUT', "DELETE"])

from application.api.review import ReviewAPI
api.add_resource(ReviewAPI, '/api/review', '/api/review/<int:response_id>', methods=['GET', 'POST', 'PUT', "DELETE"])

from application.api.deck import DownloadDeckAPI
api.add_resource(DownloadDeckAPI, '/api/download_deck/<int:deck_id>', methods=['GET'])

from application.constants import review_responses_fields

def format_report(template_file, responses={}, user={}):
    with open((template_file)) as file_:
        template = Template(file_.read())
        return template.render(responses=responses, user=user)

@app.route("/", methods=["GET"])
def  get_report():
    user = User.query.filter(User.email == "dipakpatil2615@gmail.com").first()
    reponses = marshal(user.reviewResponses.all(), review_responses_fields)
    msg = render_template("report.html", responses=reponses, user=user)
    file_name = user.email + "_monthly_report_" + str(datetime.now().date()) + ".pdf"
    render_pdf(HTML(string=msg), download_filename=file_name)
    return msg

if __name__ == "__main__":
    db.create_all()
    app.run()
