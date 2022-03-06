from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from application.error import APIException
from application.models.response_mode import ReviewCard
from application.models.response_mode import ReviewResponse
from application.models.user_mode import User
from application.models.deck import Deck, Card
from sqlalchemy.sql import func
from flask_restful import marshal, marshal_with, reqparse, Resource, fields
from application.constants import user_output_fields
from flask_security import auth_required
from flask import request

custom_user_req = reqparse.RequestParser()
custom_user_req.add_argument("id")
custom_user_req.add_argument("email")
custom_user_req.add_argument("name")
custom_user_req.add_argument("password")
custom_user_req.add_argument("role")
custom_user_req.add_argument("email")


class UserAPI(Resource):

    @auth_required("token")
    def get(self):
        return marshal(current_user, user_output_fields)

    # @auth_required("token")
    # @marshal_with(user_output_fields)
    # def get(self):
    #     user = User.query.get(6)
    #     if user:
                    
    #         # profile = request.args.get('profile', None)
    #         # user = User.query.get(int(user_id))

    #         # if profile:
    #         #     all = current_user.reviewResponses.order_by(ReviewResponse.completed_at).all()
    #         #     final = None
    #         #     final_cards= []
    #         #     remain = []

    #         #     if all:
    #         #         final = all[-1]
    #         #         final_cards = final.cards.with_entities(ReviewCard.difficulty, func.count(ReviewCard.difficulty)).group_by(ReviewCard.difficulty).all()
    #         #         final.deck = db.session.query(Deck).filter(Deck.id==final.deck_id).first()

    #         #         all.reverse()

    #         #         if len(all) > 1:
    #         #             remain = all[1:]
                        
    #         #             for i,item in enumerate(remain):
    #         #                 remain[i].deck = db.session.query(Deck).filter(Deck.id == item.deck_id).first()
        
    #         return user, 200
    #     else:
    #         raise APIException("404", "Deck not found")

    # @marshal_with(user_output_fields)
    # def post(self):
    #     args = custom_user_req.parse_args()
    #     name = args.get("name", None)
    #     email = args.get("email", None)

    #     if name is None:
    #         raise BusinessValidationError(status_code=400, msg="name is required")

    #     if email is None:
    #         raise BusinessValidationError(status_code=400, msg="email is required")

    #     if "@" not in email:
    #         raise BusinessValidationError(status_code=400, msg="email is invalid")

    #     user = db.session.query(User).filter((User.name == name) | (User.email == email)).first()

    #     if user:
    #         raise BusinessValidationError(status_code=400, msg="User is duplicated")

    #     new_user = User(name=name, email=email)

    #     db.session.add(new_user)
    #     db.session.commit()

    #     return new_user

    # def delete(self, username):

    #     user = db.session.query(User).filter((User.name == username)).first()

    #     if user is None:
    #         raise BusinessValidationError(status_code=400, msg="User is not there")

    #     try:
    #         articles = db.session.query(Article).filter(Article.authors.any(name=username)).all()

    #         if articles and len(articles) > 0:
    #             raise BusinessValidationError(status_code=400, msg="User is arthor, can't delete him")
    #     #
    #     except:
    #         pass

    #     db.session.delete(user)
    #     db.session.commit()

    #     return "You deleted it " + username, 200

    # def put(self, username):
    #     args = custom_user_req.parse_args()
    #     email = args.get("email", None)

    #     if email is None:
    #         raise BusinessValidationError(status_code=400, msg="email is required")

    #     if "@" not in email:
    #         raise BusinessValidationError(status_code=400, msg="email is invalid")

    #     user = db.session.query(User).filter((User.name == username)).first()

    #     if user is None:
    #         raise Error_404(status_code=404)

    #     user.email = email

    #     db.session.add(user)
    #     db.session.commit()

    #     return "you updated it " + username, 200


