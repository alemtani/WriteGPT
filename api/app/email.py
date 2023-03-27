from app import mail
from flask import current_app, render_template
from flask_mail import Message
from threading import Thread

def send_async_email(app, msg):
    with app.app.context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(),msg)).start()

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[WriteGPT] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('reset_password.txt', user=user, token=token),
               text_html=render_template('reset_password.html', user=user, token=token))