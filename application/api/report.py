from flask_login import current_user
from flask_security import auth_required
from application.models.user_mode import User
from application.tasks import download_report
from flask_restful import Resource, marshal, reqparse
from flask_sse import sse

custom_req = reqparse.RequestParser()
custom_req.add_argument("isAll")
custom_req.add_argument("pdf")

class ReportAPI(Resource):

    @auth_required("token")
    def get(self, response_id):
        
        if response_id == 0:
            response_id = False
        args = custom_req.parse_args()
        isAll = bool(args.get("isAll", False))
        pdf = bool(args.get("pdf", False))
        channel=str(current_user.email) + "_" + str(current_user.id)
        sse.publish({
            "message": "Starting",
            "pdf":pdf,
            "monthly":not isAll,
            "allTime":isAll,
        }, type='report', channel=channel)
        download_report.apply_async(args=[current_user.id, response_id, isAll, pdf])

        return {"success":True, "message":"Started downloading"}, 200
    