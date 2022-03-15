from flask_login import current_user
from application.error import APIException
from application.models.response_mode import ReviewCard
from application.models.response_mode import ReviewResponse
from application.models.user_mode import User
from application.models.deck import Deck, Card
from sqlalchemy.sql import func
from flask_restful import marshal, marshal_with, reqparse, Resource, fields
from application.constants import user_output_fields, user_output_with_response_fields
from flask_security import auth_required, hash_password, verify_password
from application.database import db
from sqlalchemy.sql import func


custom_user_req = reqparse.RequestParser()

custom_user_req.add_argument("name")
custom_user_req.add_argument("currentPassword")
custom_user_req.add_argument("newPassword")
custom_user_req.add_argument("confirmNewPassword")
custom_user_req.add_argument("role")
custom_user_req.add_argument("isAll")


class UserAPI(Resource):

    @auth_required("token")
    def get(self):
        args = custom_user_req.parse_args()
        isAll = args.get("isAll", False)
        
        if isAll:
            resp = marshal(current_user, user_output_with_response_fields)
        else:
            resp = marshal(current_user, user_output_fields)

        return resp, 200


    @auth_required("token")
    def put(self):
        
        try:
            user = current_user

            args = custom_user_req.parse_args()
            user.username = args.get("name", user.username)

            user.role = args.get('role', user.role)
            
            currentPassword = args.get('currentPassword', None)
            if currentPassword:
                print(currentPassword)
                if verify_password(currentPassword, user.password):
                    newPassword = args.get('newPassword', None)
                    confirmNewPassword = args.get('confirmNewPassword', None)

                    
                    if newPassword and confirmNewPassword and len(newPassword) > 7 and len(newPassword) < 16:
                        if newPassword != confirmNewPassword:
                            raise Exception('Passwords not matching')
                        
                        user.password = hash_password(newPassword)
                    else:
                        raise Exception("Password must be at least 8 and at max 15 letters long")
                else:
                    raise Exception('Current password is wrong')

            db.session.add(user)
            db.session.commit()
            return marshal(user, user_output_fields), 200
        except Exception as e:
            db.session.rollback()
            return APIException(400, str(e)).error, 400
        


