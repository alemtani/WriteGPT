from app import mail
from flask import current_app, render_template
from flask_mail import Message
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, template, **kwargs):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = render_template(f'{template}.txt', **kwargs)
    msg.html = render_template(f'{template}.html', **kwargs)
    Thread(target=send_async_email, args=(current_app._get_current_object(),msg)).start()