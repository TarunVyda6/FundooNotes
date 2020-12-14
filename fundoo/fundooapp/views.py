# Create your views here.

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
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account
from .serializers import RegisterSerializer, SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer, \
    EmailVerificationSerializer, LoginSerializer
from .utils import Util


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        """
        it verifies the credentials, if credentials were matched then returns data in json format, else throws exception
        :return: return json data if credentials are matched
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        """
        it takes user details and it will create account for user
        :rtype: user data and its status if credentials are valid
        """
        serializer = self.serializer_class(data=request.data)
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
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):

        """
        it verifies for credentials, if credentials are in correct format then after email verification user will have access to login
        :rtype: user data and its status if credentials are valid
        """
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = Account.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.is_active = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': 'some other issue'}, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        """
        it takes email id as input and sends verification email link
        :rtype: it returns a response message saying verification link is sent to mail
        """
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
            Util.send_email(data)
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response({'Failed': "Email id you have entered doesn't exist"}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
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
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        """
        it take new password and confirm password and if the password matches all criteria then it will set new password
        :rtype: data of the user and its success status
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
