from application.models.deck import Card, Deck
from .models.user_mode import User
from .models.response_mode import ReviewCard, ReviewResponse
from flask_restful import fields
from application.database import db


deck_cards_fields = {
    'id': fields.Integer,
    'options': fields.String,
    'front': fields.String,
    # 'back': fields.String,
    'deck_id': fields.Integer,
    'created_by_id': fields.Integer
}

deck_output_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "created_for": fields.String(attribute=lambda obj: str(Deck.Type(obj.created_for).name)),
    "public_status": fields.Boolean,
    "created_at":fields.DateTime,
    "created_by_id": fields.Integer,
    "cards":fields.List(fields.Nested(deck_cards_fields), attribute=lambda obj: obj.cards.all() ),
    "number_of_cards": fields.Integer,
    "user":fields.Nested({"username":fields.String})
}

review_card_fields = {
    "id": fields.Integer,
    "correct_option": fields.String,
    "correct": fields.Boolean,
    "time": fields.Integer,
    "selected_option": fields.String,
    "difficulty": fields.String(attribute=lambda obj1: str(ReviewCard.Diffculty(obj1.difficulty).name)),
    "completed_at":fields.DateTime,
    "review_respose_id": fields.Integer,
    "card_id": fields.Integer,
    "card": fields.Nested(deck_cards_fields, attribute=lambda obj: db.session.query(Card).filter(Card.id==obj.card_id).first()),
}


review_responses_fields = {
    "id": fields.Integer,
    "avg_time": fields.Float,
    "score": fields.Integer,
    "user_id": fields.Integer,
    "completed_at":fields.DateTime,
    "deck_id": fields.Integer,
    "deck": fields.Nested(deck_output_fields, attribute=lambda obj:db.session.query(Deck).filter(Deck.id==obj.deck_id).first()),
    "cards": fields.List(fields.Nested(review_card_fields), attribute=lambda obj: obj.cards.order_by(ReviewCard.completed_at.desc()).all() ),
    "avg_time_count":fields.Float(attribute=lambda obj: obj.avg_time_count()),
}

user_output_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "role": fields.String(attribute=lambda obj: str(User.Role(obj.role).name)),
    "created_at":fields.DateTime,
    "review_response":fields.Float(attribute=lambda obj: obj.review_response())
}


user_output_with_response_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "role": fields.String(attribute=lambda obj: str(User.Role(obj.role).name)),
    "created_at":fields.DateTime,
    "response":fields.List(fields.Nested(review_responses_fields), 
        attribute=lambda obj: obj.reviewResponses.order_by(ReviewResponse.completed_at.desc()).all() 
    ),
    "review_response":fields.Float(attribute=lambda obj: obj.review_response())
}


#  fields.List(fields.Nested(program_student), required=True, description='List of students on program',
#                         attribute=lambda obj: obj.get_students())