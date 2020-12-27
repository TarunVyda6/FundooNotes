from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from fundooapp.views import RegisterView
from rest_framework import status
import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestViews:

    def test_valid_user_details_for_registration(self, client):
        """
        Ensure we can create a new account object.
        """
        path = reverse('register')
        valid_registration_data = {'first_name': "tarun",
                                   'last_name': "vyda",
                                   'email': "kamaltarun.rao0@gmail.com",
                                   'user_name': "tarunvyda",
                                   'password': "adminpass"}
        response = client.post(path, data=valid_registration_data, format='json')
        assert response.status_code == 201

    def test_invalid_user_details_for_registration(self, client):
        """
        Ensure we cannot create a new account object with invalid credentials
        """
        invalid_registration_data = {'first_name': "abc",
                                     'last_name': "def",
                                     'email': "abc123@gmail.com",
                                     'user_name': "abcdef"}

        response = client.post(reverse('register'), invalid_registration_data, format='json')
        assert response.status_code == 400

    def test_valid_user_for_login(self, client):
        """
        Ensure we can login with valid credentials.
        """
        valid_registration_data = {'first_name': "tarun",
                                   'last_name': "vyda",
                                   'email': "kamaltarun.rao0@gmail.com",
                                   'user_name': "tarunvyda",
                                   'password': "adminpass"}
        valid_login_data = {
            'email': "kamaltarun.rao0@gmail.com",
            'password': "adminpass"}

        client.post(reverse('register'), valid_registration_data, format='json')
        user = User.objects.filter(email=valid_registration_data['email']).first()
        user.is_active = True
        user.save()
        response = client.post(reverse('login'), valid_login_data, format='json')
        assert response.status_code == 200

    def test_given_invalid_credentials_for_login(self, client):
        """
        Ensure we cannot login with invalid credentials.
        """
        valid_registration_data = {'first_name': "tarun",
                                   'last_name': "vyda",
                                   'email': "kamaltarun.rao0@gmail.com",
                                   'user_name': "tarunvyda",
                                   'password': "adminpass"}
        invalid_login_data = {'email': "kamaltarun.rao0@gmail.com",
                              'password': "adminpa"}

        client.post(reverse('register'), valid_registration_data, format='json')
        user = User.objects.filter(email=valid_registration_data['email']).first()
        user.is_active = True
        user.save()

        response = client.post(reverse('login'), invalid_login_data, format='json')
        assert response.status_code == 400
