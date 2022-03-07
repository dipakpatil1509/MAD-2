from flask_login import current_user
from application.error import APIException
from application.models.response_mode import ReviewCard
from application.models.response_mode import ReviewResponse
from application.models.user_mode import User
from application.models.deck import Deck, Card
from sqlalchemy.sql import func
from flask_restful import marshal, marshal_with, reqparse, Resource, fields
from application.constants import user_output_fields, review_responses_fields, review_card_fields
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
        resp = marshal(current_user, user_output_fields)
        if isAll:
            all = current_user.reviewResponses.order_by(ReviewResponse.completed_at).all()
            final = None
            final_cards= []
            remain = []

            if all:
                final = all[-1]
                final_cards = final.cards.with_entities(ReviewCard.difficulty, func.count(ReviewCard.difficulty)).group_by(ReviewCard.difficulty).all()
                final.deck = db.session.query(Deck).filter(Deck.id==final.deck_id).first()

                all.reverse()

                if len(all) > 1:
                    remain = all[1:]
                    
                    for i,item in enumerate(remain):
                        remain[i].deck = db.session.query(Deck).filter(Deck.id == item.deck_id).first()
                
                resp['final'] = marshal(final, review_responses_fields) 
                resp['final_cards'] = marshal(final_cards, review_card_fields) 
                resp['solved_decks']= marshal(remain, review_responses_fields) 

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
            return marshal(user, user_output_fields)
        except Exception as e:
            db.session.rollback()
            return APIException(400, str(e)).error
        


