from django.core.mail import EmailMessage
import threading
from services.myexceptions import (InvalidCredentials, UnVerifiedAccount, EmptyField, LengthError)


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()


class Validation:
    def validate_data(data):
        if 'email' not in data or data['email'] is '':
            raise EmptyField('email field should not be empty')
        if 'password' not in data or data['password'] is '':
            raise EmptyField('password field should not be empty')
        return True

    def validate_register(data):
        if len(data['email']) > 50:
            raise LengthError('email maximum length should be 50 character')
        if len(data['password']) > 68 and len(data['password'] <= 6):
            raise LengthError('email maximum length should be 50 character')
        if len(data['last_name']) > 20:
            raise LengthError('lastname maximum length should be 20 character')
        if len(data['user_name']) > 20:
            raise LengthError('username maximum length should be 20 character')
        return True
