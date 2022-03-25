from datetime import datetime
from flask_restful import marshal
from pytz import timezone
from application.api.profile import daily_remainder_msg, google_chat_send, new_deck_added
from application.models.user_mode import User, Webhooks
from application.workers import celery
from application.models.response_mode import ReviewResponse
from celery.schedules import crontab
from application.database import db
from sqlalchemy import func
from application.constants import email_sendgrid_send, format_message, sms_send, webhooks_fields

@celery.on_after_finalize.connect
def periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0, hour=17), 
        daily_remainders.s(), 
        name="daily remainders"
    )
    sender.add_periodic_task(
        crontab(minute=17, hour=22, day_of_week="*", day_of_month=1), 
        monthly_reports.s(), 
        name="monthly reports"
    )

@celery.task()
def send_google_chat(url, msg):
    google_chat_send(url, msg)

@celery.task()
def send_email(address, subject, file, data):
    email_sendgrid_send(
        to_address=address, 
        subject=subject, 
        message=format_message(file, data=data)
    )

@celery.task()
def send_sms(number, msg):
    sms_send(number, msg)

@celery.task
def daily_remainders():

    users_who_not_completed_today = db.session.execute('''
        SELECT * FROM user WHERE user.id NOT IN (
            SELECT reviewresponse.user_id FROM reviewresponse
            WHERE DATE(reviewresponse.completed_at) = :DATE_1
        )
    ''', {'DATE_1':datetime.now(timezone('Asia/Kolkata')).date()})

    for user in users_who_not_completed_today:
        webhooks = Webhooks.query.filter(Webhooks.user == user.id).all()
        
        for webhook in webhooks:
            send_google_chat.apply_async(args=[webhook.url, daily_remainder_msg(user)])
        
        send_email.apply_async(args=[
            user.email,
            "Missing you today!",
            "daily_remainder.html",
            {
                "name":user.username if user.username else user.email
            }
        ])
        if user.mobile_number:
            send_sms.apply_async(args=[user.mobile_number, '''
                Hope you are doing well!!!

                Hey `{user.username}`, you haven't solved any deck today. Is everything ok? Do let us know in case you are not fine. We care about you.
                Please come back as soon as possible.

                Best Regards,
                Dipak Patil
            '''])

    return True

@celery.task()
def monthly_reports():

    users = User.query.all()

    for user in users:
        print(user.reviewResponses)


@celery.task()
def notify_users(deck):

    webhooks = Webhooks.query.filter(Webhooks.notify==True).all()

    for webhook in webhooks:
        user = User.query.filter(User.id==webhook.user).first()
        if user.id != deck['created_by_id']:
            send_google_chat.apply_async(args=[webhook.url, new_deck_added(user, deck)])
        
