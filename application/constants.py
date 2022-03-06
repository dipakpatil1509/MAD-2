from .models.user_mode import User
from .models.response_mode import ReviewCard
from flask_restful import fields

deck_cards_fields = {
    'id': fields.Integer,
    'options': fields.List(fields.String),
    'front': fields.String,
    'back': fields.String,
    'deck_id': fields.Integer,
    'created_by_id': fields.Integer
}

deck_output_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "created_for": fields.String([x.name for x in User.Role]),
    "public_status": fields.Boolean,
    "created_at":fields.DateTime,
    "created_by_id": fields.Integer,
    "cards":fields.List(fields.Nested(deck_cards_fields))
}

review_card_fields = {
    "id": fields.Integer,
    "correct_option": fields.String,
    "created_for": fields.String([x.name for x in User.Role]),
    "correct": fields.Boolean,
    "time": fields.Integer,
    "selected_option": fields.String,
    "difficulty": fields.String([x.name for x in ReviewCard.Diffculty]),
    "completed_at":fields.DateTime,
    "review_respose_id": fields.Integer,
    "card_id": fields.Integer,
}


review_responses_fields = {
    "id": fields.Integer,
    "avg_time": fields.Float,
    "score": fields.Integer,
    "user_id": fields.Integer,
    "completed_at":fields.DateTime,
    "deck_id": fields.Integer,
    "cards": fields.List(fields.Nested(review_card_fields)),
    "avg_time_count":fields.Float,
}

user_output_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "fs_uniquifier": fields.String,
    "role": fields.String([x.name for x in User.Role]),
    "created_at":fields.DateTime,
    "decks":fields.List(fields.Nested(deck_output_fields)),
    "reviewResponses":fields.List(fields.Nested(deck_output_fields)),
    "review_response":fields.Float(attribute=lambda obj: obj.review_response())
}
#  fields.List(fields.Nested(program_student), required=True, description='List of students on program',
#                         attribute=lambda obj: obj.get_students())