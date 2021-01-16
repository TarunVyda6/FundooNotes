from celery import shared_task
from django.core.mail import EmailMessage
import threading
from notes.views import Reminder


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


@shared_task
def send_email(data):
    """
        sends email on the basis of set data in calling view
    """
    email = EmailMessage(
        subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
    EmailThread(email).start()


@shared_task()
def email_reminder():
    """
        performs repeated task of sending email to all users who have reminders
    """
    Reminder.email_reminder()
