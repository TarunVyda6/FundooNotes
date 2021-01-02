from .models import Account
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
import jwt
from services.myexceptions import (InvalidCredentials, UnVerifiedAccount, EmptyField, ValidationError)


class RegisterSerializer(ModelSerializer):
    """
    this serializer class is used for serialization and deserialization of data while registering
    """
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'user_name', 'password']

    def validate(self, attrs):
        """
        it verifies credentials, if credentials are in correct format then after email verification it will create account for user
        :rtype: user data and its status if credentials are valid
        """
        email = attrs.get('email', '')
        user_name = attrs.get('user_name', '')

        if not user_name.isalnum():
            raise ValidationError('username should contain only alphanumeric characters')
        return attrs

    def create(self, validated_data):
        """
        this method will create an account for validated data
        """
        return Account.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    """
    this serializer class is used for serialization and deserialization of data at email verification
    """
    token = serializers.CharField(max_length=555)

    class Meta:
        model = Account
        fields = ['token']


class LoginSerializer(ModelSerializer):
    """
    this serializer class is used for serialization and deserialization of data while login
    """
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    user_name = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    class Meta:
        model = Account
        fields = ['email', 'password', 'user_name']

    def validate(self, attrs):
        """
        it verifies the credentials, if credentials were matched then returns data in json format, else throws exception
        :return: return json data if credentials are matched
        """
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise InvalidCredentials('email or password is incorrect')
        if not user.is_verified:
            raise UnVerifiedAccount('please verify your account first to login')

        return {
            'email': user.email
        }


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    """
    this serializer class is used for serialization and deserialization of data while requesting for reset password
    """
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    """
    this serializer class is used for serialization and deserialization of data while setting new password
    """
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        """
        it take new password and confirm password and if the password matches all criteria then it will set new password
        :rtype: data of the user and its success status
        """
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
