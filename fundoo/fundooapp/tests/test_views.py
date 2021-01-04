from django.urls import reverse
from rest_framework import status
import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

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
        self.note_archived_url = reverse("archived")
        self.single_note_archived_url = 'http://127.0.0.1:8000/note/archived/2'
        self.note_pinned_url = reverse("pinned")
        self.single_note_pinned_url = 'http://127.0.0.1:8000/note/pinned/4'
        self.note_trash_url = reverse("trash")
        self.single_note_trash_url = 'http://127.0.0.1:8000/note/trash/6'

        self.valid_label_data = {
            'label_name': "Third Note",
        }

        self.valid_note_data = {
            "title": "my testing note",
            "description": "this is my second note",
            "is_archived" : True,
            "is_pinned" : True,
            "label": ["Third Note"],
            "collaborate": ["kamaltarun.rao0@gmail.com"]
        }
        self.valid_note_data2 = {
            "title": "valid note",
            "description": "this is my valid note",
            "trash" : True,
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

    def test_register_view_with_valid_details(self):
        """
        Ensure we can create a new account object and it returns status code as 201.
        """

        response = self.client.post(self.register_url, self.valid_registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_view_with_invalid_details(self):
        """
        Ensure we cannot create a new account object and returns status code as 400.
        """

        response = self.client.post(self.register_url, self.invalid_registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTest(Data):

    def test_login_api_view_with_valid_details(self):
        """
        Ensure we can login and return status code as 200.
        """
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.save()
        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_api_view_with_invalid_details(self):
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
    """
    Test case for validating Labels class with valid and invalid details.
    """
    def test_labels_with_valid_details(self):
        """
        Test case for validating Labels class with valid details.
        """
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

        client = APIClient()
        response = client.put(self.label_url, self.valid_label_put_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete(self.label_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_labels_with_invalid_details(self):
        """
        Test case for validating Labels class with invalid details.
        """
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


class NotesTest(Data):
    """
    Test case for validating Notes class with valid and invalid details.
    """
    def test_notes_with_valid_details(self):
        """
        Test case for validating Labels class with valid details.
        """
        client = APIClient()
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.save()
        response = client.post(self.login_url, self.valid_login_data, format='json')
        headers = response.data['data']['token']

        response = self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = client.post(self.note_post_url, self.valid_note_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = client.get(self.note_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.put(self.note_url, self.valid_note_put_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.delete(self.note_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_notes_with_invalid_details(self):
        """
        Test case for validating Labels class with invalid details.
        """
        client = APIClient()
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.save()
        response = client.post(self.login_url, self.valid_login_data, format='json')
        headers = response.data['data']['token']

        response = self.client.post(self.note_post_url, self.invalid_note_data, HTTP_AUTHORIZATION=headers,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(self.note_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(self.note_url, self.valid_note_put_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.delete(self.note_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ArchivedViewTest(Data):
    """
    Test case for validating ArchivedViewTest class with valid and invalid details.
    """

    def test_archived_view_for_valid_details(self):
        """
        Test case for validating ArchivedView class with valid details.
        """
        client = APIClient()
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.save()
        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = response.data['data']['token']
        self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data2, HTTP_AUTHORIZATION=headers, format='json')

        response = client.get(self.note_archived_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get(self.single_note_archived_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PinnedViewTest(Data):
    """
    Test case for validating PinnedView class with valid and invalid details.
    """
    def test_pinned_view_for_valid_details(self):
        """
        Test case for validating PinnedView class with valid details.
        """
        client = APIClient()
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.save()
        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = response.data['data']['token']
        self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data2, HTTP_AUTHORIZATION=headers, format='json')

        response = client.get(self.note_pinned_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get(self.single_note_pinned_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TrashViewTest(Data):

    def test_trash_view_for_valid_details(self):
        client = APIClient()
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.save()
        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = response.data['data']['token']
        self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data2, HTTP_AUTHORIZATION=headers, format='json')

        response = self.client.get(self.note_trash_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.single_note_trash_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
