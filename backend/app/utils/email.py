from flask import current_app
from flask_mail import Message
from app.extensions import mail
from threading import Thread

def send_async_email(app, msg):
    """Send email asynchronously."""
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            current_app.logger.error(f"Failed to send email: {str(e)}")

def send_email(subject, recipients, html_body, text_body=None, sender=None):
    """Send an email."""
    if not isinstance(recipients, list):
        recipients = [recipients]
    
    msg = Message(
        subject=subject,
        recipients=recipients,
        sender=sender or current_app.config['MAIL_DEFAULT_SENDER']
    )
    
    msg.html = html_body
    if text_body:
        msg.body = text_body
    
    # Send email in a background thread
    Thread(
        target=send_async_email,
        args=(current_app._get_current_object(), msg)
    ).start() 