from flask_login import current_user
from flask_login.utils import logout_user
from flask_restful import Resource
from flask_security import auth_required
from application.constants import email_send, format_message
        
class Logout(Resource):

    @auth_required("token")
    def get(self):
        logout_user()
        return {"success":True}, 200
    
class WelcomeEmail(Resource):

    @auth_required("token")
    def get(self):
        try:
            email_send(
                current_user.email, 
                "Welcome to Flashcard!", 
                format_message("welcome.html", data={
                    "name":current_user.username if current_user.username else current_user.email
                })
            )
        except Exception as e:
            print(e)
        return {"success":True}, 200