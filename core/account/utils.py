import sendgrid
import os
from sendgrid.helpers.mail import *

class Util:
    @staticmethod
    def send_email(data):
        try:
            sg = sendgrid.SendGridAPIClient(api_key=os.getenv('EMAIL_KEY'))
            mail = Mail(
                from_email=Email(os.getenv('EMAIL_FROM'),name=os.getenv('EMAIL_SENDER_NAME')),
                to_emails=To(data['to_email']),
                subject=data['email_subject'],
                plain_text_content=data['email_body'],
            )
            return sg.client.mail.send.post(request_body=mail.get()).status_code == 202
        except Exception as e:
            print(e)
            return False