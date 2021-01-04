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
class Data(TestCase):
    """
    this class will initialise all the urls and data and it is inherited by other test classes
    """

    def setUp(self):
        """
        this method setup all the url and data which was required by all test cases
        """
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.valid_registration_data = {'first_name': "tarun",
                                        'last_name': "vyda",
                                        'email': "kamaltarun.rao0@gmail.com",
                                        'user_name': "tarunvyda",
                                        'password': "adminpass"}
        self.invalid_registration_data = {'first_name': "abc",
                                          'last_name': "def",
                                          'email': "abc123@gmail.com",
                                          'user_name': "abcdef"}
        self.valid_login_data = {
            'email': "kamaltarun.rao0@gmail.com",
            'password': "adminpass"}
        self.invalid_login_data = {
            'email': "kamaltarun.rao0@gmail.com",
            'password': "adminpa"}

        self.note_post_url = reverse("note")
        self.note_url = 'http://127.0.0.1:8000/note/1'
        self.label_post_url = reverse("label-post")

        self.valid_label_data = {
            'label_name': "Third Note",
        }

        self.valid_note_data = {
            "title": "my testing note",
            "description": "this is my second note",
            "label": ["Third Note"],
            "collaborate": ["kamaltarun.rao0@gmail.com"]
        }
        self.valid_note_put_data = {
            "title": "testing note",
            "description": "this is changed note",
        }
        self.invalid_note_data = {
            'description': "this is my second note",
            'label': "Third Note",
            'collaborate': ["kamaltarun.rao0@gmail.com"],
        }
        self.label_url = 'http://127.0.0.1:8000/label/1'

        self.valid_label_put_data = {'label_name': "First Note",
                                     }
        self.invalid_label_data = {'label': "Third Note",
                                   }


class RegistrationTests(Data):
    """
    this class will test registration view and match with status_code
    """

    def test_given_valid_details_for_registration(self):
        """
        Ensure we can create a new account object and it returns status code as 201.
        """

        response = self.client.post(self.register_url, self.valid_registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_given_invalid_details_for_registration(self):
        """
        Ensure we cannot create a new account object and returns status code as 400.
        """

        response = self.client.post(self.register_url, self.invalid_registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTest(Data):

    def test_given_valid_credentials_login(self):
        """
        Ensure we can login and return status code as 200.
        """

        self.client.post(self.register_url, self.valid_registration_data, format='json')
        # user = mixer.blend('fundooapp.Account')
        # user = User.objects.filter(email=user.email).first()
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.save()
        # print(type(user.email))
        # data = {'email' : user.email, 'password' : user.password}
        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        # response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_given_invalid_credentials_for_login(self):
        """
        Ensure we cannot login and returns status code as 400.
        """

        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_active = True
        user.save()

        response = self.client.post(self.login_url, self.invalid_login_data, format='json')
        assert response.status_code == 400


class LabelTest(Data):

    def test_given_valid_label_details_for_crud(self):
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.save()
        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = response.data['data']['token']
        response = self.client.post(self.label_post_url, self.valid_label_data, HTTP_AUTHORIZATION=headers,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.label_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response = self.client.put(self.label_url, self.valid_label_put_data, HTTP_AUTHORIZATION=headers, format='json')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete(self.label_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_given_invalid_label_details_for_crud(self):
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.save()
        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = response.data['data']['token']
        response = self.client.post(self.label_post_url, self.invalid_label_data, HTTP_AUTHORIZATION=headers,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(self.label_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.put(self.label_url, self.valid_label_put_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.delete(self.label_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# class NotesTest(Data):
#
#     def test_given_valid_note_url_for_crud(self):
#         self.client.post(self.register_url, self.valid_registration_data, format='json')
#         user = User.objects.filter(email=self.valid_registration_data['email']).first()
#         user.is_verified = True
#         user.save()
#
#         response = self.client.post(self.login_url, self.valid_login_data, format='json')
#         token = response.data['data']['token']
#         headers = str(token)
#         response = self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=headers, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         response=self.client.post(self.note_post_url, self.valid_note_data, HTTP_AUTHORIZATION=headers, format='json')
#         print(response.data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # response = self.client.get(self.note_url, HTTP_AUTHORIZATION=headers, format='json')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        #
        # response = self.client.put(self.note_url, self.valid_note_put_data, HTTP_AUTHORIZATION=token, format='json')
        # print(response.data)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #
        # response = self.client.delete(self.note_url, format='json')
        # self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    # def test_given_invalid_note_details_for_crud(self):
    #     response = self.client.post(self.note_post_url, self.invalid_note_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    #     response = self.client.get(self.note_url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    #     response = self.client.put(self.note_url, self.valid_note_put_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    #     response = self.client.delete(self.note_url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
