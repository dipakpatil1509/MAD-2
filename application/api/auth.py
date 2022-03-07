from flask_login.utils import login_required, logout_user
from flask_restful import Resource, abort, marshal
from application.models.user_mode import User
from flask_security import auth_required
from flask_security.forms import RegisterForm, NullableStringField

        
class Logout(Resource):

    @auth_required("token")
    def get(self):
        logout_user()
        return {"success":True}, 200