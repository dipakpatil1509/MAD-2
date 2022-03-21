import json
from flask_login import current_user
from flask_restful import Resource, marshal, reqparse
from flask_security import auth_required
from application.models.user_mode import User
from application.models.deck import Deck,Card
from application.database import db
from application.error import APIException
from sqlalchemy.exc import IntegrityError
from application.constants import AESCipher, deck_output_fields
from hmac import new
from hashlib import sha256


deck_req = reqparse.RequestParser()
deck_req.add_argument("name")
deck_req.add_argument("public_status")
deck_req.add_argument("created_for")

class DeckAPI(Resource):
    
    @auth_required("token")
    def get(self, deck_id):
        deck = None
        try:
            deck_curr = db.session.query(Deck).filter(Deck.id == int(deck_id)).first()
            if deck_curr:
                deck_curr.user = db.session.query(User).with_entities(User.username).filter(User.id == deck_curr.created_by_id).first()
                deck_curr.number_of_cards = deck_curr.cards.count()
                deck=marshal(deck_curr, deck_output_fields)
                return deck
            else:
                raise APIException("404", "Deck not found")
        except APIException as e:
            print(e)
            return e.error, e.error["error_code"]
        except Exception as e:
            print(e)
            return APIException(400, str(e)).error, 400

    @auth_required("token")
    def post(self):
        try:

            args = deck_req.parse_args()
            name = args.get("name", None)
            public_status = args.get("public_status", None)
            created_for = args.get("created_for", None)

            if name == "" or name is None or not isinstance(name, str) or name.isnumeric():
                raise APIException("400","Deck Name is required and should be string.")

            deck_curr = db.session.query(Deck).filter(Deck.name == name).first()

            if deck_curr:
                raise APIException("409", "Deck already exist")

            if created_for and (not isinstance(created_for, str) or created_for.isnumeric()):
                raise APIException("400","Deck Created for should be string.")

            user_curr = current_user

            if user_curr is None:
                raise APIException("404", "User not found")
            
            print(created_for)
            new_deck = Deck(
                name=name,
                public_status=bool(int(public_status)), 
                created_by_id=current_user.id, 
                created_for=(created_for or "ALL")
            )

            db.session.add(new_deck)
            db.session.commit()

            return marshal(new_deck, deck_output_fields), 200
        except APIException as e:
            return e.error, e.error["error_code"]
        except Exception as e:
            return APIException(400, str(e)).error, 400

    @auth_required("token")
    def put(self, deck_id):
    
        try:
            args = deck_req.parse_args()
            name = args.get("name", None)
            public_status = args.get("public_status", None)
            created_for = args.get("created_for", None)

            if name == "" or name is None or not isinstance(name, str) or name.isnumeric():
                raise APIException("400","Deck Name is required and should be string.")

            deck_curr = db.session.query(Deck).filter(Deck.id == int(deck_id) and Deck.created_by_id==current_user).first()

            if deck_curr is None:
                raise APIException("404", "Deck not found")

            deck_curr.name = name

            if public_status:
                deck_curr.public_status = bool(int(public_status))

            if created_for:
                deck_curr.created_for = created_for
            else:
                deck_curr.created_for = "ALL"


            db.session.add(deck_curr)
            db.session.commit()

            return marshal(deck_curr, deck_output_fields)
        except IntegrityError:
            return APIException("400", "Deck name already exists").error, 400
        except APIException as e:
            return e.error, e.error["error_code"]
        except Exception as e:
            return APIException("400", str(e)).error, 400


    @auth_required("token")
    def delete(self, deck_id):

        deck_curr = db.session.query(Deck).filter(Deck.id == int(deck_id) and Deck.created_by_id==current_user.id).first()

        if deck_curr is None:
            return APIException(404, "Deck not found").error, 404

        db.session.delete(deck_curr)
        db.session.commit()

        return {"status":True, "message":"Successfully Deleted"}, 200

class DownloadDeckAPI(Resource):

    @auth_required("token")
    def get(self, deck_id):
        deck = None
        try:
            deck_curr = db.session.query(Deck).filter(Deck.id == int(deck_id)).first()
            if deck_curr:
                deck_curr.user = db.session.query(User).with_entities(User.username).filter(User.id == deck_curr.created_by_id).first()
                deck_curr.number_of_cards = deck_curr.cards.count()
                deck=marshal(deck_curr, deck_output_fields)
                deck = json.dumps(deck)
                deck = AESCipher("c8XaaKx^jafq2f9yw*CNaOAye#Y#b2eF").encrypt(deck)
                print(AESCipher("c8XaaKx^jafq2f9yw*CNaOAye#Y#b2eF").decrypt(deck))
                return {"status":True, "deck":deck}, 200
            else:
                raise APIException("404", "Deck not found")
        except APIException as e:
            print(e)
            return e.error, e.error["error_code"]
        except Exception as e:
            print(e)
            return APIException(400, str(e)).error, 400



