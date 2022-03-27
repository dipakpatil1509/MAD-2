import base64
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta
from flask_restful import marshal
from pytz import timezone
from application.api.profile import daily_remainder_msg, google_chat_send, new_deck_added
from application.models.deck import Deck
from application.models.user_mode import User, Webhooks
from application.workers import celery
from application.models.response_mode import ReviewResponse
from celery.schedules import crontab
from application.database import db
import pandas as pd
import base64
from io import BytesIO
from flask_sse import sse
from application.constants import deck_output_fields, email_sendgrid_send, format_message, get_report, get_report_html, sms_send, webhooks_fields

@celery.on_after_finalize.connect
def periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0, hour=17), 
        daily_remainders.s(), 
        name="daily remainders"
    )
    sender.add_periodic_task(
        crontab(minute=0, hour=0, day_of_week="*", day_of_month=1), 
        monthly_reports.s(), 
        name="monthly reports"
    )

@celery.task()
def send_google_chat(url, msg, link=None):
    google_chat_send(url, msg, link)

@celery.task()
def send_email(address, subject, file, data, attachment=None, filename=None):
    email_sendgrid_send(
        to_address=address, 
        subject=subject, 
        message=format_message(file, data=data),
        attachment=attachment, filename=filename
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
            send_google_chat.apply_async(args=[webhook.url, daily_remainder_msg(user), "http://localhost:8080/"])
        
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
    today = date.today()
    first = today.replace(day=1)

    last_month_last_day = first - timedelta(days=1)
    last_month_first_day = last_month_last_day.replace(day=1)

    users = User.query.all()

    lower_limit = date(
        year=last_month_first_day.year, 
        month=last_month_first_day.month, 
        day=last_month_first_day.day
    )

    upper_limit = date(
        year=last_month_last_day.year, 
        month=last_month_last_day.month, 
        day=last_month_last_day.day
    )

    for user in users:
        responses = user.reviewResponses.filter(
            ReviewResponse.completed_at >= lower_limit,
            ReviewResponse.completed_at <= upper_limit
        ).all()
        pdf = get_report(user, responses)
        pdf = base64.b64encode(pdf).decode()
        print("pdf created")
        send_email.apply_async(args=[
            user.email,
            "Monthly Progress Report",
            "monthly_report.html",
            {
                "name":user.username if user.username else user.email
            },
            pdf,
            user.email + "_monthly_report_" + str(today) + ".pdf"
        ])


@celery.task()
def notify_users(deck):

    webhooks = Webhooks.query.filter(Webhooks.notify==True).all()

    for webhook in webhooks:
        user = User.query.filter(User.id==webhook.user).first()
        if user.id != deck['created_by_id']:
            send_google_chat.apply_async(args=[webhook.url, new_deck_added(user, deck), "http://localhost:8080/view_deck/{deck_id}"])

@celery.task()
def download_report(user_id, review_id=None, all_time=None, pdf=None):
    
    user = User.query.filter(User.id == user_id).first()

    channel=str(user.email) + "_" + str(user.id)
    sse.publish({
        "message": "Started downloading",
        "pdf":pdf,
    }, type='report', channel=channel)

    if review_id:
        responses = user.reviewResponses.filter(ReviewResponse.id == review_id).all()
    elif all_time:
        responses = user.reviewResponses.all()
    else:
        today = date.today()
        last_month_day = today + relativedelta(months=-1)

        lower_limit = date(
            year=last_month_day.year, 
            month=last_month_day.month, 
            day=last_month_day.day
        )

        upper_limit = date(
            year=today.year, 
            month=today.month, 
            day=today.day
        )

        responses = user.reviewResponses.filter(
            ReviewResponse.completed_at >= lower_limit,
            ReviewResponse.completed_at <= upper_limit
        ).all()
    
    if pdf:
        sse.publish({
            "message": "Converting to pdf",
            "pdf":pdf,
            "monthly":not all_time,
            "allTime":all_time,
        }, type='report', channel=channel)
        file = get_report(user, responses)
        file = base64.b64encode(file).decode()
        print("pdf created")
    else:
        sse.publish({
            "message": "Converting to html",
            "pdf":pdf,
            "monthly":not all_time,
            "allTime":all_time,
        }, type='report', channel=channel)
        file = get_report_html(user, responses)
    
    sse.publish({
        "message": "Processing for download", 
        "file":file,
        "pdf":pdf,
        "monthly":not all_time,
        "allTime":all_time,
    }, type='report', channel=channel)


@celery.task()
def download_excel(user_id, decks=[]):
    
    user = User.query.filter(User.id == user_id).first()

    channel=str(user.email) + "_" + str(user.id)

    for i, deck_id in enumerate(decks):
        deck = None
        deck_curr = db.session.query(Deck).filter(Deck.id == int(deck_id)).first()
        if deck_curr:
            deck_curr.user = db.session.query(User).with_entities(User.username).filter(User.id == deck_curr.created_by_id).first()
            deck_curr.number_of_cards = len(deck_curr.cards)
            deck=marshal(deck_curr, deck_output_fields)
        cards = deck["cards"]
        if len(cards) > 0:
            df = pd.DataFrame.from_dict(cards)
            df = df.drop(['id', 'deck_id', 'created_by_id'], axis=1)
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine="xlsxwriter")
            df.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            output.seek(0)
            file = base64.b64encode(output.read()).decode()
            sse.publish({
                "message": str(i+1) + " of " + str(len(decks)) + " downloaded", 
                "filename":f'{deck["name"]} cards.xlsx',
                "file":file, 
                "isDone":i+1 == len(decks),
            }, type='excel', channel=channel)

        sse.publish({
            "message": str(i+1) + " of " + str(len(decks)) + " downloaded",
            "isDone":i+1 == len(decks),
        }, type='excel', channel=channel)