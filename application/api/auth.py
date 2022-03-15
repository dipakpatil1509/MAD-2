from flask_login.utils import logout_user
from flask_restful import Resource
from flask_security import auth_required

        
class Logout(Resource):

    @auth_required("token")
    def get(self):
        logout_user()
        return {"success":True}, 200