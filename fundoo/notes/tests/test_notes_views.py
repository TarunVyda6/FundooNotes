from django.urls import reverse
from rest_framework import status
import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import json

User = get_user_model()

client = APIClient()


@pytest.mark.django_db()
class Data(TestCase):
    """
    this class will initialise all the urls and data and it is inherited by other test classes
    """

    def setUp(self):
        """
        this method setup all the url and data which was required by all test cases
        """
        self.register_url = reverse("register")
        self.valid_registration_data = {'first_name': "tarun",
                                        'last_name': "vyda",
                                        'email': "kamaltarun.rao0@gmail.com",
                                        'user_name': "tarunvyda",
                                        'password': "adminpass"}
        self.valid_test_registration_data = {'first_name': "virat",
                                             'last_name': "kohli",
                                             'email': "viratkohli123@gmail.com",
                                             'user_name': "viratkohli",
                                             'password': "adminpass"}

        self.login_url = reverse("login")

        self.valid_login_data = {
            'email': "kamaltarun.rao0@gmail.com",
            'password': "adminpass"}
        self.note_post_url = reverse("note")
        self.note_url = reverse("single-note", kwargs={"pk": 1})

        self.valid_label_data = {
            'label_name': "Third Note",
        }

        self.valid_note_data = {
            "title": "my testing note",
            "description": "this is my second note",
            "is_archived": True,
            "is_pinned": True,
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

        self.label_url = reverse('label', kwargs={'pk': 1})

        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.save()

        self.logged_in = self.client.post(self.login_url, self.valid_login_data, format='json')
        self.headers = self.logged_in.data['data']['token']


class NotesTest(Data):
    """
    Test case for validating Notes class with valid and invalid details.
    """

    def test_notes_with_valid_details(self):
        """
        Test case for validating Labels class with valid details.
        """
        response = self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=self.headers,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = client.post(self.note_post_url, self.valid_note_data, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = client.get(self.note_url, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = client.get(self.note_url, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = client.get(self.note_post_url, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.put(self.note_url, self.valid_note_put_data, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.delete(self.note_url, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_notes_with_invalid_details(self):
        """
        Test case for validating Labels class with invalid details.
        """

        response = self.client.post(self.note_post_url, self.invalid_note_data, HTTP_AUTHORIZATION=self.headers,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.get(self.note_url, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(self.note_url, self.valid_note_put_data, HTTP_AUTHORIZATION=self.headers,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.delete(self.note_url, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ArchivedViewTest(Data):
    """
    Test case for validating ArchivedViewTest class with valid and invalid details.
    """

    def test_archived_view_for_valid_details(self):
        """
        Test case for validating ArchivedView class with valid details.
        """

        self.valid_note_data2 = {
            "title": "valid note",
            "description": "this is my valid note",
            "trash": True,
            "label": ["Third Note"],
            "collaborate": ["kamaltarun.rao0@gmail.com"]
        }

        self.note_archived_url = reverse("archived")
        self.single_note_archived_url = reverse("single-archived", kwargs={"pk": 2})

        self.logged_in = self.client.post(self.login_url, self.valid_login_data, format='json')
        self.headers = self.logged_in.data['data']['token']
        self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=self.headers, format='json')
        client.post(self.note_post_url, self.valid_note_data, HTTP_AUTHORIZATION=self.headers, format='json')
        client.post(self.note_post_url, self.valid_note_data2, HTTP_AUTHORIZATION=self.headers, format='json')

        response = client.get(self.note_archived_url, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get(self.single_note_archived_url, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PinnedViewTest(Data):
    """
    Test case for validating PinnedView class with valid and invalid details.
    """

    def test_pinned_view_for_valid_details(self):
        """
        Test case for validating PinnedView class with valid details.
        """

        self.valid_note_data2 = {
            "title": "valid note",
            "description": "this is my valid note",
            "trash": True,
            "label": ["Third Note"],
            "collaborate": ["kamaltarun.rao0@gmail.com"]
        }
        self.note_pinned_url = reverse("pinned")
        self.single_note_pinned_url = reverse("single-pinned", kwargs={"pk": 4})

        self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=self.headers, format='json')
        client.post(self.note_post_url, self.valid_note_data, HTTP_AUTHORIZATION=self.headers, format='json')
        client.post(self.note_post_url, self.valid_note_data2, HTTP_AUTHORIZATION=self.headers, format='json')

        client.post(self.note_post_url, self.valid_note_data2, format='json')

        response = client.get(self.note_pinned_url, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get(self.single_note_pinned_url, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TrashViewTest(Data):

    def test_trash_view_for_valid_details(self):
        """
        Test case for validating TrashView class with valid details.
        """

        self.valid_note_data2 = {
            "title": "valid note",
            "description": "this is my valid note",
            "trash": True,
            "label": ["Third Note"],
            "collaborate": ["kamaltarun.rao0@gmail.com"]
        }

        self.note_trash_url = reverse("trash")
        self.single_note_trash_url = reverse("single-trash", kwargs={"pk": 6})

        self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=self.headers, format='json')
        client.post(self.note_post_url, self.valid_note_data2, HTTP_AUTHORIZATION=self.headers, format='json')

        response = self.client.get(self.note_trash_url, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.single_note_trash_url, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SearchNoteTest(Data):

    def test_search_note_for_valid_details(self):
        """
        Test case for validating SearchNote class with valid details.
        """
        self.search_note_url = reverse("search") + "?q=my second"
        self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=self.headers, format='json')
        client.post(self.note_post_url, self.valid_note_data, HTTP_AUTHORIZATION=self.headers, format='json')
        response = client.get(self.search_note_url, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_note_with_no_details(self):
        """
        Test case for validating PinnedView class without providing details.
        """
        self.empty_search_note_url = reverse("search") + "?q="
        self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=self.headers, format='json')
        client.post(self.note_post_url, self.valid_note_data, HTTP_AUTHORIZATION=self.headers, format='json')
        response = client.get(self.empty_search_note_url, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
