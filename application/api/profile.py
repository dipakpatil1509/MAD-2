from json import dumps
from application.cache import cache
from flask_login import current_user
from application.error import APIException
from application.models.deck import Deck
from application.models.user_mode import  User, Webhooks
from flask_restful import marshal, reqparse, Resource
from application.constants import user_output_fields, user_output_with_response_fields, webhooks_fields, deck_output_fields
from flask_security import auth_required, hash_password, verify_password
from application.database import db
from flask import request
import requests


custom_user_req = reqparse.RequestParser()

custom_user_req.add_argument("name")
custom_user_req.add_argument("currentPassword")
custom_user_req.add_argument("newPassword")
custom_user_req.add_argument("confirmNewPassword")
custom_user_req.add_argument("role")
custom_user_req.add_argument("isAll")
custom_user_req.add_argument("mobile_number")

def welcome_msg(user):
    return '''
*Welcome to flashcard family!*
Hope you are doing well!!!

Hey `{name}`, This message confirms that you webhook has started working.
If you have opted out for notifications for deck, you will receive messages every time someone adds a deck.

If it's not you, please remove this webhook from your space and contact me.

Best Regards,
Dipak Patil
21f1004451@student.onlinedegree.iitm.ac.in
'''.format(name=user.username if user.username else "Flashcard user")


def new_deck_added(user, deck):
    return '''
*A new deck added*
Hope you are doing well!!!

Hey `{name}`, a new public deck, {deck_name}, is added by {deck_owner}. If you are a {deck_role}, it's probably for you.
Please <http://localhost:8080/view_deck/{deck_id}|check out > as soon as possible.

If you have not subscribe to this message, please contact me.

Best Regards,
Dipak Patil
21f1004451@student.onlinedegree.iitm.ac.in
'''.format(
    name=user.username if user.username else user.email,
    deck_name=deck['name'],
    deck_owner=deck['user']['username'] if deck['user']['username'] else deck['user']['email'],
    deck_role=deck['created_for'],
    deck_id=deck['id']
)

def daily_remainder_msg(user):
    return '''
*Daily Remainder*
Hope you are doing well!!!

Hey `{name}`, you haven't solved any deck today. Is everything ok? Do let us know in case you are not fine. We care about you.
Please <http://localhost:8080/|come back > as soon as possible.

Best Regards,
Dipak Patil
21f1004451@student.onlinedegree.iitm.ac.in
'''.format(
    name=user.username if user.username else user.email,
)

def google_chat_send(url, message=None, link=None):
    url = url

    bot_message = {}

    if link:
        bot_message["buttons"]= [
            {
                "textButton": {
                    "text": "Solve now",
                    "onClick": {
                        "openLink": {
                        "url": link
                        }
                    }
                }
            }
        ]
    
    if message:
        bot_message['text'] = message

    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    response = requests.post(url, headers=message_headers, data=dumps(bot_message) )

    return response

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

            user.mobile_number = args.get('mobile_number', None)

            currentPassword = args.get('currentPassword', None)
            if currentPassword:
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
        

class WebhooksAPI(Resource):
    @auth_required("token")
    def get(self):
        return marshal(current_user.webhooks.all(), webhooks_fields), 200

    @auth_required("token")
    def post(self):
        
        try:
            user = current_user

            args = request.get_json()
            hooks = args.get('hooks', [])
            
            flag = self.deleteWebhook(hooks, user)

            response_list = []

            if flag:
                response_list.append({"status":True, "message":"Successfully deleted blank inputs"})

            for i, hook in enumerate(hooks):
                message = ""
                flag = False
                
                if "url" in hook and hook["url"]:
                    if "id" in hook and hook["id"]:
                        message, flag = self.updateWebhook(hook, user)
                    else:
                        message, flag = self.createWebHook(hook, user)
                    response_list.append({
                        "status":flag,
                        "message":"Webhook " + str(i+1) + ": " + message
                    })
            
            return {"data": response_list}, 200
        except Exception as e:
            return APIException(400, str(e)).error, 400

    def createWebHook(self, hook, user):

        webhook = user.webhooks.filter(Webhooks.url == hook["url"]).first()

        if webhook:
            return "Already added", False
        
        response = google_chat_send(hook["url"], message=welcome_msg(user))

        if response.status_code == 200:
            new_hook = Webhooks(
                url=hook["url"],
                notify=hook["notify"],
                user=user.id
            )

            db.session.add(new_hook)
            db.session.commit()
            return "Succesfully added with " + str(response.status_code), True
        else:
            data = response.json();
            return "Failed with " + str(response.status_code) + ". " + data['error']['message'], False

    def updateWebhook(self, hook, user):
        
        
        webhook = db.session.query(Webhooks).filter(Webhooks.user == user.id).filter(Webhooks.id == int(hook["id"])).first()

        if webhook:
            if webhook.url != hook["url"]:
                response = google_chat_send(hook["url"], message=welcome_msg(user))

                if response.status_code == 200:
                    webhook.url = hook["url"]
                else:
                    data = response.json();
                    return "Failed with " + str(response.status_code) + ". " + data['error']['message']
            
            if webhook.notify != hook["notify"]:
                webhook.notify = hook["notify"]

            db.session.add(webhook)
            db.session.commit()

            return "Successfully updated", True
        else:
            return self.createWebHook(hook, user)
       
    def deleteWebhook(self, hooks, user):
        
        ids = [hook['id'] for hook in hooks]
        webhook = user.webhooks.filter(~(Webhooks.id.in_(ids))).all()

        if len(webhook) > 0:
            for hook in webhook :
                db.session.delete(hook)
            db.session.commit()
            return True
        else:
            return False