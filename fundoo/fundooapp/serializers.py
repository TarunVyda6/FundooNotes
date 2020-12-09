from .models import NewUser
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed



class UserDetailsSerializer(ModelSerializer):
    class Meta:
        model = NewUser
        fields = '__all__'


class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = NewUser
        fields = ['first_name', 'last_name', 'email', 'user_name', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        user_name = attrs.get('user_name', '')

        if not user_name.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return NewUser.objects.create_user(**validated_data)


class LoginSerializer(ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    user_name = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    class Meta:
        model = NewUser
        fields = ['email', 'password', 'user_name']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')

        return {
            'user_name': user.user_name, 'email': user.email,
        }

