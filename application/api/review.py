from datetime import datetime
from application.cache import cache
from flask_login import current_user
from flask_restful import Resource, marshal, reqparse
from flask_security import auth_required
from pytz import timezone
from application.models.response_mode import ReviewCard, ReviewResponse
from application.models.user_mode import User
from application.models.deck import Deck,Card
from application.database import db
from application.error import APIException
from sqlalchemy.exc import IntegrityError
from application.constants import review_card_fields, review_responses_fields

card_req = reqparse.RequestParser()
card_req.add_argument("card_id")
card_req.add_argument("answer")
card_req.add_argument("time")
card_req.add_argument("difficulty")

@cache.memoize(timeout=60*60)
def get_review(response_id):
    try:
        response_curr = db.session.query(ReviewResponse).filter(ReviewResponse.id == response_id).first()
        if response_curr:
            return marshal(response_curr, review_responses_fields)
        else:
            raise APIException("404", "Response not found")
    except APIException as e:
        return e.error, e.error["error_code"]
    except Exception as e:
        return APIException(400, str(e)).error, 400

class ReviewAPI(Resource):
    
    @auth_required("token")
    def get(self, response_id):
        return get_review(response_id)

    @auth_required("token")
    def post(self):
        try:
            args = card_req.parse_args()
            card_id = args.get('card_id')
            answer = args.get('answer')
            time_take = args.get('time')

            correct = False
            
            if card_id is None or not isinstance(card_id, str):
                raise APIException("400","Card id is required.")

            card = db.session.query(Card).filter(Card.id == int(card_id)).first()

            if answer == "" or answer is None or not isinstance(answer, str):
                raise APIException("400","Answer is required")

            if time_take == "" or time_take is None or not isinstance(time_take, str):
                raise APIException("400","Time is required")

            if str(card.back).lower() == answer.strip().lower():
                correct = True

            
            response_curr = db.session.query(ReviewResponse).filter(ReviewResponse.user_id == current_user.id).filter(ReviewResponse.deck_id == int(card.deck_id)).first()

            print(response_curr)
            if not response_curr:
                response_curr = ReviewResponse(
                    score = 0,
                    avg_time = 0,
                    user_id = int(current_user.id),
                    deck_id = int(card.deck_id),
                )
                db.session.add(response_curr)
                db.session.commit()
            

            new_response = ReviewCard(
                correct_option = str(card.back),
                selected_option = answer,
                time = int(time_take),
                correct = correct,
                card_id = int(card_id),
                review_respose_id = int(response_curr.id)
            )

            db.session.add(new_response)
            db.session.commit()
            
            response_curr.score = round((response_curr.cards.filter(ReviewCard.correct == True).count()/response_curr.cards.count()) * 100, 2)
            
            response_curr.avg_time = response_curr.avg_time_count()/response_curr.cards.count()

            response_curr.completed_at = datetime.now(timezone('Asia/Kolkata'))
            
            db.session.add(response_curr)
            db.session.commit()

            res = {
                "status":True,
                "correct":correct,
                "answer":card.back,
                "response":marshal(response_curr, review_responses_fields),
                "card":marshal(new_response, review_card_fields)
            }

            return res, 200
        
        except IntegrityError as e:
            return APIException("400", "Already submitted").error, 400
        except Exception as e:
            print(e)
            return APIException("400", str(e)).error, 400

    
    @auth_required("token")
    def put(self, response_id):
        try:
            args = card_req.parse_args()
            difficulty = args.get('difficulty')
            
            if difficulty == "" or difficulty is None or not isinstance(difficulty, str):
                raise APIException("400","Difficulty level is required")

            review_res_curr = db.session.query(ReviewCard).filter(ReviewCard.id == response_id).first()
            
            if review_res_curr:
                review_res_curr.difficulty = ReviewCard.Diffculty(difficulty).name

                db.session.add(review_res_curr)
                db.session.commit()
            else:
                raise APIException("404","Response card not found")

            res = {
                "status":True,
            }

            return res, 200
        
        except IntegrityError as e:
            return APIException("400", "Already submitted").error, 400
        except Exception as e:
            print(e)
            return APIException("400", str(e)).error, 400
