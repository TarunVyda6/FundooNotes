import os
import jwt
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import (generics, status, views)
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account
from .serializers import RegisterSerializer, SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer, \
    EmailVerificationSerializer, LoginSerializer
# from .utils import Util
import logging
from services.cache import Cache
from decouple import config
from rest_framework.exceptions import AuthenticationFailed
from notes import utils
from services.encrypt import Encrypt
from services.exceptions import (MyCustomError, ExceptionType)
from .utils import Validation
from .tasks import send_email

logging.basicConfig(filename='users.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class LoginAPIView(generics.GenericAPIView):
    """
    this class will check credentials and if valid it will allow user to login
    """
    serializer_class = LoginSerializer

    def post(self, request):
        """
        it verifies the credentials, if credentials were matched then returns data in json format, else throws exception
        :return: return json data if credentials are matched
        """
        try:
            data = request.data
            if Validation.validate_data(data):
                serializer = self.serializer_class(data=data)
                serializer.is_valid(raise_exception=True)
                user = Account.objects.get(email=serializer.data['email'])
                token = Encrypt.encode(user.id)
                cache = Cache()
                cache.set_cache("TOKEN_" + str(user.id) + "_AUTH", token)
                result = {'token': token}
                return utils.manage_response(status=True, message="login successful", data=result,
                                             status_code=status.HTTP_200_OK)
        except MyCustomError as e:
            return utils.manage_response(status=False, message=e.message, exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return utils.manage_response(status=False, message='some other issue please try after some time',
                                         exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.GenericAPIView):
    """
    this class will register a new account
    """
    serializer_class = RegisterSerializer

    def post(self, request):
        """
        it takes user details and it will create account for user
        :rtype: user data and its status if credentials are valid
        """
        try:
            data = request.data
            if Validation.validate_data(data) and Validation.validate_register(data):
                serializer = self.serializer_class(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                user_data = serializer.data
                user = Account.objects.get(email=user_data['email'])
                token = RefreshToken.for_user(user).access_token
                absolute_url = request.build_absolute_uri(reverse('email-verify')) + "?token=" + str(token)
                email_body = 'Hi ' + user.user_name + \
                             ', \n Use the link below to verify your email \n' + absolute_url
                data = {'email_body': email_body, 'to_email': user.email,
                        'email_subject': 'Verify your email'}
                send_email.delay(data)
                return utils.manage_response(status=True, message="Account created successfully", data=user_data,
                                             status_code=status.HTTP_201_CREATED)
        except MyCustomError as e:
            return utils.manage_response(status=False, message=e.message, exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return utils.manage_response(status=False, message='some other issue please try after some time',
                                         exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(views.APIView):
    """
    this class will verifies the email
    """
    serializer_class = EmailVerificationSerializer

    def get(self, request):

        """
        it verifies for credentials, if credentials are in correct format then after email verification user will have access to login
        :rtype: user data and its status if credentials are valid
        """
        token = request.GET.get('token')
        result = {'message': 'some other issue',
                  'status': False}
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = Account.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.is_active = True
                user.save()
                result['message'] = 'Successfully activated'
                result['status'] = True
                return utils.manage_response(status=result['status'], message=result['message'],
                                             status_code=status.HTTP_200_OK)
            else:
                result['message'] = 'email is already verified'
                return utils.manage_response(status=result['status'], message=result['message'],
                                             status_code=status.HTTP_400_BAD_REQUEST)

        except jwt.ExpiredSignatureError as e:
            result['message'] = 'Activation Expired'
            return utils.manage_response(status=result['status'], message=result['message'],
                                         exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            result['message'] = 'Invalid Token'
            return utils.manage_response(status=result['status'], message=result['message'],
                                         exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return utils.manage_response(status=result['status'], message=result['message'],
                                         exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(generics.GenericAPIView):
    """
    this class will request for new password
    """
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        """
        it takes email id as input and sends verification email link
        :rtype: it returns a response message saying verification link is sent to mail
        """
        result = {'message': 'some other issue',
                  'status': False}
        try:
            email = request.data.get('email', '')

            if Account.objects.filter(email=email).exists():
                user = Account.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                redirect_url = reverse('password-reset-complete')
                absolute_url = request.build_absolute_uri(reverse('password-reset-confirm'))
                email_body = 'Hello, \n Your token number is : ' + token + ' \n your uidb64 code is ' + uidb64 + ' \n Use link below to reset your password  \n' + \
                             absolute_url + "?redirect_url=" + redirect_url
                data = {'email_body': email_body, 'to_email': user.email,
                        'email_subject': 'Reset your passsword'}
                send_email.delay(data)
                result['message'] = 'We have sent you a link to reset your password'
                result['status'] = True
                return utils.manage_response(status=result['status'], message=result['message'],
                                             status_code=status.HTTP_200_OK)
            else:
                result['message'] = "Email id you have entered doesn't exist"
                logging.debug('{}'.format(result))
                return utils.manage_response(status=result['status'], message=result['message'],
                                             status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return utils.manage_response(status=result['status'], message=result['message'],
                                         exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    """
    this class will check the token is valid or not
    """
    serializer_class = SetNewPasswordSerializer

    def get(self, request):
        """
        it checks whether the token is valid for particular user or not
        """
        redirect_url = request.GET.get('redirect_url')
        if redirect_url and len(redirect_url) > 3:
            return CustomRedirect(
                redirect_url + '?token_valid=True&message=Credentials Valid')
        else:
            return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')


class SetNewPasswordAPIView(generics.GenericAPIView):
    """
    this class will set a new password
    """
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        """
        it take new password and confirm password and if the password matches all criteria then it will set new password
        :rtype: data of the user and its success status
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return utils.manage_response(status=True, message='Password reset success',
                                     status_code=status.HTTP_200_OK)
