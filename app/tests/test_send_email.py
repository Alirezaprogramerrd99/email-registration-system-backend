import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(user_email: str, subject: str, content: str):
    msg = MIMEMultipart()
    # msg['From'] = SMTP_USER
    msg['From'] = os.environ['SMTP_USER']
    msg['To'] = user_email
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'plain'))

    # Send the email
    try:
        with smtplib.SMTP(os.environ['SMTP_SERVER'], int(os.environ['SMTP_PORT']) ) as server:
            server.starttls()
            server.login(os.environ['SMTP_USER'], os.environ['SMTP_PASSWORD'])
            server.sendmail(os.environ['SMTP_USER'], user_email, msg.as_string())
        print(f"Email sent to {user_email}")

    except Exception as e:
        print(f"Failed to send email to {user_email}: {e}")


if __name__ == "__main__":
    send_email('arashidi1378@gmail.com', 'Test email from no-reply', 'Test content ...')