from application.api.deck import get_deck
from application.cache import cache
from flask import request
from flask_login import current_user
from flask_restful import Resource, marshal, reqparse
from flask_security import auth_required
from application.models.deck import Deck,Card
from application.database import db
from application.error import APIException
from sqlalchemy.exc import IntegrityError
from application.constants import deck_cards_fields
import pandas as pd

card_req = reqparse.RequestParser()
card_req.add_argument("front")
card_req.add_argument("back")
card_req.add_argument("options")
card_req.add_argument("deck_id")

@cache.memoize(timeout=24*60*60)
def get_cards(card_id):
    try:
        card_curr = db.session.query(Card).filter(Card.id == int(card_id)).first()
        if card_curr:
            card_curr.deck = db.session.query(Deck).filter(Deck.id == card_curr.deck_id).first()
            card = marshal(card_curr, deck_cards_fields)
            card['back'] = card_curr.back
            return card, 200
        else:
            raise APIException("404", "Card not found")
    except APIException as e:
        return e.error, e.error["error_code"]
    except Exception as e:
        return APIException(400, str(e)).error, 400


class CardAPI(Resource):
    
    @auth_required("token")
    def get(self, card_id):
        return get_cards(card_id)

    @auth_required("token")
    def post(self):
        try:
            args = card_req.parse_args()
            front = args.get("front", None)
            back = args.get("back", None)
            options = args.get("options", None)
            deck_id = args.get("deck_id", None)

            if front == "" or front is None or not isinstance(front, str):
                raise Exception("Front is required.")
            
            if back == "" or back is None or not isinstance(back, str):
                raise Exception("Back is required.")
            
            if options == "" or options is None or not isinstance(options, str) or options.isnumeric():
                raise Exception("Options should be string.")
        
            user = current_user.id
            new_card = Card(
                front=front,
                back= back, 
                options = options,
                deck_id=int(deck_id), 
                created_by_id=user
            )

            db.session.add(new_card)
            db.session.commit()

            return {
                "success":True,
                "data":marshal(new_card, deck_cards_fields)
            }, 201

        except Exception as e:
            return APIException("400", str(e)).error, 400

    @auth_required("token")
    def put(self, card_id):
        try:
            args = card_req.parse_args()
            front = args.get("front", None)
            back = args.get("back", None)
            options = args.get("options", None)
            deck_id = args.get("deck_id", None)

            if front == "" or front is None or not isinstance(front, str):
                raise Exception("Front is required.")

            if back == "" or back is None or not isinstance(back, str):
                raise Exception("Back is required.")

            if options == "" or options is None or not isinstance(options, str) or options.isnumeric():
                raise Exception("Options should be string.")

            card_curr = db.session.query(Card).filter(Card.id == int(card_id)).first()

            if card_curr is None:
                raise APIException("404", "Card not found")

            card_curr.front = front
            card_curr.back = back

            card_curr.options = options

            if deck_id:
                card_curr.deck_id = int(deck_id)

                db.session.add(card_curr)
                db.session.commit()

                cache.delete_memoized(get_cards, card_curr.id)
                
                return marshal(card_curr, deck_cards_fields), 200
        except IntegrityError:
            return APIException("400", "Card already exists").error, 400
        except APIException as e:
            return e.error, e.error['error_code']
        except Exception as e:
            return APIException("400", str(e)).error, 400


    @auth_required("token")
    def delete(self, card_id):

        card_curr = db.session.query(Card).filter(Card.id == int(card_id) and Card.created_by_id==current_user.id).first()

        if card_curr is None:
            return APIException(404, "Card not found").error, 404

        db.session.delete(card_curr)
        db.session.commit()

        cache.delete_memoized(get_cards, card_curr.id)

        return {"status":True, "message":"Successfully Deleted"}, 200


class UploadAPI(Resource):

    @auth_required("token")
    def post(self):
        try:
            deck_id = request.form.get("deck_id")
            file = request.files.get('importFile')
            excel = pd.read_excel(file)
            skipped_rows = 0
            for i, item in excel.iterrows():
                try:  
                    front = item['front']
                    back = item['back']
                    options = item['options']
                    if front == "" or front is None:
                        raise Exception("Front is necessay")
                    
                    if back == "" or back is None:
                        raise Exception("Back is required.")
                    
                    if options == "" or options is None or not isinstance(options, str):
                        raise Exception("Options are required and should be string.")

                    user = current_user.id
                    new_card = Card(
                        front=front,
                        back= back, 
                        options = options,
                        deck_id=int(deck_id), 
                        created_by_id=user
                    )

                    db.session.add(new_card)
                    db.session.commit()

                    cache.delete_memoized(get_deck, int(deck_id))

                except Exception as e:
                    print(str(e))
                    skipped_rows += 1

            return {
                'success': True,
                'message': f'Successfully Added Cards. Skipped Rows {skipped_rows}',
            }, 200
        except APIException as e:
            return e.error, e.error["error_code"]
        except Exception as e:
            return APIException("400", str(e)).error, 400

