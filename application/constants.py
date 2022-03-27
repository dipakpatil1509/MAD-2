from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from flask import render_template
from application.models.deck import Card, Deck
from .models.user_mode import User
from .models.response_mode import ReviewCard, ReviewResponse
from flask_restful import fields, marshal
from application.database import db
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from weasyprint import HTML

SMS_API_KEY="HXIN1728258019IN"
SMS_API_SECRET="Afb79b5e96ed71649fe6dfa162cf04425"
SENDER_ADDRESS="noreply@flashcard.com"
SMTP_SERVER_HOST="localhost"
SMTP_SERVER_PORT = 1025
SENDER_PASSWORD = ""
SENDGRID_API = "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"


webhooks_fields = {
    'id': fields.Integer,
    "url":fields.String,
    "notify":fields.Boolean,
    'user': fields.Integer,
}

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
    "cards":fields.List(fields.Nested(deck_cards_fields), attribute=lambda obj: obj.cards ),
    "number_of_cards": fields.Integer,
    "user":fields.Nested({
        "username":fields.String, 
        "email":fields.String
    }, attribute=lambda obj: db.session.query(User).filter(User.id==obj.created_by_id).first())
}

class MyDateFormat(fields.Raw):
    def format(self, value):
        return value.strftime('%H:%M:%S, %d/%m/%Y')

review_card_fields = {
    "id": fields.Integer,
    "correct_option": fields.String,
    "correct": fields.Boolean,
    "time": fields.Integer,
    "selected_option": fields.String,
    "difficulty": fields.String(attribute=lambda obj1: str(ReviewCard.Diffculty(obj1.difficulty).name)),
    "completed_at":MyDateFormat,
    "review_respose_id": fields.Integer,
    "card_id": fields.Integer,
    "card": fields.Nested(deck_cards_fields, attribute=lambda obj: db.session.query(Card).filter(Card.id==obj.card_id).first()),
}


review_responses_fields = {
    "id": fields.Integer,
    "avg_time": fields.Float,
    "score": fields.Integer,
    "user_id": fields.Integer,
    "completed_at":MyDateFormat,
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
    "mobile_number":fields.String,
    "response":fields.List(fields.Nested(review_responses_fields), 
        attribute=lambda obj: obj.reviewResponses.order_by(ReviewResponse.completed_at.desc()).all() 
    ),
    "review_response":fields.Float(attribute=lambda obj: obj.review_response())
}

# class ReportGenerate:
def format_message(template_file, data={}):
    return render_template(template_file, data=data)

def email_send(to_address, subject, message, attachment=None):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "html"))

    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)

    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

    return True

def email_sendgrid_send(to_address, subject, message, attachment=None, filename=None):
    message = Mail(
        from_email='dipakpatil2415@gmail.com',
        to_emails=to_address,
        subject=subject,
        html_content=message,
    )
    print("message created")
    if attachment:
        from sendgrid.helpers.mail import Attachment, FileContent, FileName, FileType, Disposition
        attachedFile = Attachment(
            FileContent(attachment),
            FileName(filename),
            FileType('application/pdf'),
            Disposition('attachment')
        )
        message.attachment = attachedFile
    try:
        sg = SendGridAPIClient(SENDGRID_API)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
        print(e.message)

def sms_send(number, message):
    try:
        print(number, message)
        headers = {}
        headers["api-key"] = SMS_API_SECRET
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        data = "to=" + str(number[1:]) + "&sender=KLRHXA&source=API&type=TXN&template_id=1107160466944278506&body=" + message

        print(data)
        response = requests.post(
            "https://api.kaleyra.io/v1/" + SMS_API_KEY + "/messages",
            headers=headers,
            data=data
        )
        print(response.json())
    except Exception as ex:
        print('Error creating batch: %s' % str(ex))

def get_report_html(user, reviewResp):
    reponses = marshal(reviewResp, review_responses_fields)
    user = marshal(user, user_output_fields)
    msg = render_template("report.html", responses=reponses, user=user)
    return msg

def get_report(user, reviewResp):
    msg = get_report_html(user,reviewResp)
    html = HTML(string=msg)
    return html.write_pdf()

