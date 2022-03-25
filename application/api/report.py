from crypt import methods
from flask_login import current_user
from application.error import APIException
from application.models.user_mode import  User
from flask_restful import marshal, Resource
from flask_security import auth_required
from application.database import db
from flask import request, render_template
from flask import current_app as app

@app.route("/", methods=["GET"])
def  get_report():
    user = User.query.filter(User.email == "dipakpatil2615@gmail.com").first()
    return render_template("report.html", responses=user.reviewResponses.all())

# class ReportAPI(Resource):

#     @auth_required("token")
#     def get(self):
#         print(current_user.webhooks.all())
#         return marshal(current_user.webhooks.all(), webhooks_fields), 200

#     @auth_required("token")
#     def post(self):
        
#         try:
#             user = current_user

#             args = request.get_json()
#             hooks = args.get('hooks', [])
            
#             flag = self.deleteWebhook(hooks, user)

#             response_list = []

#             if flag:
#                 response_list.append({"status":True, "message":"Successfully deleted blank inputs"})

#             for i, hook in enumerate(hooks):
#                 message = ""
#                 flag = False
                
#                 if "url" in hook and hook["url"]:
#                     if "id" in hook and hook["id"]:
#                         message, flag = self.updateWebhook(hook, user)
#                     else:
#                         message, flag = self.createWebHook(hook, user)
#                     response_list.append({
#                         "status":flag,
#                         "message":"Webhook " + str(i+1) + ": " + message
#                     })
            
#             return {"data": response_list}, 200
#         except Exception as e:
#             return APIException(400, str(e)).error, 400

#     def createWebHook(self, hook, user):

#         webhook = user.webhooks.filter(Webhooks.url == hook["url"]).first()

#         if webhook:
#             return "Already added", False
        
#         response = google_chat_send(hook["url"], message=welcome_msg(user))

#         if response.status_code == 200:
#             new_hook = Webhooks(
#                 url=hook["url"],
#                 notify=hook["notify"],
#                 user=user.id
#             )

#             db.session.add(new_hook)
#             db.session.commit()
#             return "Succesfully added with " + str(response.status_code), True
#         else:
#             data = response.json();
#             return "Failed with " + str(response.status_code) + ". " + data['error']['message'], False

#     def updateWebhook(self, hook, user):
        
        
#         webhook = db.session.query(Webhooks).filter(Webhooks.user == user.id).filter(Webhooks.id == int(hook["id"])).first()

#         if webhook:
#             if webhook.url != hook["url"]:
#                 response = google_chat_send(hook["url"], message=welcome_msg(user))

#                 if response.status_code == 200:
#                     webhook.url = hook["url"]
#                 else:
#                     data = response.json();
#                     return "Failed with " + str(response.status_code) + ". " + data['error']['message']
            
#             if webhook.notify != hook["notify"]:
#                 webhook.notify = hook["notify"]

#             db.session.add(webhook)
#             db.session.commit()

#             return "Successfully updated", True
#         else:
#             return self.createWebHook(hook, user)
       
#     def deleteWebhook(self, hooks, user):
        
#         ids = [hook['id'] for hook in hooks]
#         webhook = user.webhooks.filter(~(Webhooks.id.in_(ids))).all()

#         if len(webhook) > 0:
#             for hook in webhook :
#                 db.session.delete(hook)
#             db.session.commit()
#             return True
#         else:
#             return False