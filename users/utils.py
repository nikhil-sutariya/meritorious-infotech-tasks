from django.core.mail import EmailMessage
import threading
import os

from_email = os.getenv('EMAIL_HOST_USERNAME')

class Utils:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
                subject=data['email_subject'], 
                body=data['email_body'], 
                from_email=str(from_email),
                to=[data['to_email']]
            )
        email.content_subtype ="html"
        if data.get('file_name'):
            email.attach_file(data['file_name'])
        thread = threading.Thread(target=email.send)
        thread.start()
