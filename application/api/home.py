from application.cache import cache
from flask_login import current_user
from application.error import APIException
from application.models.user_mode import User
from application.models.deck import Deck
from flask_restful import marshal, reqparse, Resource
from application.constants import deck_output_fields
from flask_security import auth_required
from application.database import db



home_req = reqparse.RequestParser()
home_req.add_argument("flag")

@cache.cached(timeout=60)
def get_public_deck():
    return db.session.query(Deck).filter(Deck.public_status == True).all()

class Home(Resource):
    
    @auth_required("token")
    def get(self):
        args = home_req.parse_args()
        flag = args.get('flag')
        decks = []
        
        try:
            if flag is None or flag == "0":
                decks = get_public_deck()
            elif flag == "1":
                decks = db.session.query(Deck).filter(Deck.public_status == True).filter(Deck.created_for.in_(i for i in Deck.Type if i.value == current_user.role.value)).all()
            elif flag == "2":
                decks = current_user.decks.all()
            elif flag == "3":
                decks = current_user.decks.filter(Deck.public_status == False).all()
            
            for i, item in enumerate(decks):
                decks[i].user = db.session.query(User).with_entities(User.username).filter(User.id == item.created_by_id).first()
                decks[i].number_of_cards = len(item.cards)
            
            return marshal(decks, deck_output_fields)
        except Exception as e:
            print(e)
            return APIException(400, str(e)).error, 400