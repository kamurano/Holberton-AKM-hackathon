import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import url_for

from secret.mail import MAIL_FROM, SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD

def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = MAIL_FROM
    msg['To'] = to_email

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(MAIL_FROM, to_email, msg.as_string())
        
        
def send_verification_email(email, token):
    verification_url = url_for('auth_controller.verify_email', token=token, _external=True)
    subject = "Email Verification"
    body = f"Please click the link to verify your email: {verification_url}"
    send_email(email, subject, body)
    

def send_email_html(to_email, subject, body):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = MAIL_FROM
    msg['To'] = to_email
    
    msg.attach(MIMEText(body, 'html'))



    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(MAIL_FROM, to_email, msg.as_string())
    

def send_phishing_mail(email):
    subject = "LinkedIn Email"
    with open('api/static/linkedin/linkedin.html', 'r') as f:
        body = f.read()
    send_email_html(email, subject, body)