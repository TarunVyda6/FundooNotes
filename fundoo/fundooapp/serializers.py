from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import Account


class RegisterSerializer(ModelSerializer):
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
        try:
            user_name = attrs.get('user_name', '')

            if not user_name.isalnum():
                raise serializers.ValidationError(
                    self.default_error_messages)
            return attrs
        except Exception:
            raise AuthenticationFailed('some other issue', 401)
    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = Account
        fields = ['token']


class LoginSerializer(ModelSerializer):
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
            raise AuthenticationFailed('Invalid credentials, try again')

        return {
            'user_name': user.user_name,
            'email': user.email,
        }

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
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
