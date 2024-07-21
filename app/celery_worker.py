from celery import Celery
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.utils import crud
from app.model import models
from celery.schedules import crontab
import os
from dotenv import load_dotenv


# Create a Celery instance
celery_app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

load_dotenv()

@celery_app.task
def send_email_task(user_email: str, subject: str, content: str):
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = os.environ['SMTP_USER']
    msg['To'] = user_email
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'plain'))

    # Send the email
    try:
        with smtplib.SMTP(os.environ['SMTP_SERVER'], int(os.environ['SMTP_PORT'])) as server:
            server.starttls()
            server.login(os.environ['SMTP_USER'], os.environ['SMTP_PASSWORD'])
            server.sendmail(os.environ['SMTP_USER'], user_email, msg.as_string())
        print(f"Email sent to {user_email}")
    except Exception as e:
        print(f"Failed to send email to {user_email}: {e}")

@celery_app.task
def check_and_send_emails():
    db: Session = SessionLocal()
    
    try:
        # Retrieve unsent letters
        letters = crud.get_unsent_latters(db)
        for letter in letters:
            users = crud.get_users(db)
            for user in users:
                send_email_task.delay(user.email, letter.title, letter.content)
            
            crud.mark_letter_as_sent(db, letter.id)
    finally:
        db.close()

@celery_app.task
def send_past_emails_to_new_user(user_id: int):
    db: Session = SessionLocal()

    try:
        # Retrieve the user
        user = crud.get_user(db, user_id)
        
        # Retrieve letters from the past month
        letters = crud.get_letters_from_last_month(db)
        for letter in letters:
            send_email_task.delay(user.email, letter.title, letter.content)
    finally:
        db.close()


# celery_app.conf.beat_schedule = {
#     'send-emails-every-few-hours': {
#         'task': 'app.celery_worker.check_and_send_emails',
#         'schedule': crontab(hour='*/2'),  # Every 2 hours
#     },
# }

celery_app.conf.beat_schedule = {
    'send-emails-every-few-minute': {
        'task': 'app.celery_worker.check_and_send_emails',
        'schedule': crontab(minute='*/10'),  # Every 10 minutes.
    },
}

celery_app.conf.timezone = 'UTC'