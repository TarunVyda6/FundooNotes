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
        self.invalid_registration_data_password_missing = {'first_name': "abc",
                                                           'last_name': "def",
                                                           'email': "abc123@gmail.com",
                                                           'user_name': "abcdef"}
        self.invalid_registration_data_email_missing = {'first_name': "abc",
                                                        'last_name': "def",
                                                        'password': "adminpass",
                                                        'user_name': "abcdef"}
        self.invalid_test_registration_data_email_length = {'first_name': "virat",
                                                            'last_name': "kohli",
                                                            'email': "viratkohli123viratkohli123viratkohli123viratkohli123viratkohli123viratkohli123viratkohli123viratkohli123viratkohli123viratkohli123viratkohli123viratkohli123viratkohli123viratkohli123viratkohli123viratkohli123viratkohli123viratkohli123@gmail.com",
                                                            'user_name': "viratkohli",
                                                            'password': "adminpass"}
        self.invalid_test_registration_data_password_less_than_6 = {'first_name': "virat",
                                                                    'last_name': "kohli",
                                                                    'email': "viratkohli123@gmail.com",
                                                                    'user_name': "viratkohli",
                                                                    'password': "admin"}
        self.invalid_test_registration_data_user_name_greater_than_20 = {'first_name': "virat",
                                                                         'last_name': "kohli",
                                                                         'email': "viratkohli123@gmail.com",
                                                                         'user_name': "viratkohliviratkohliviratkohli",
                                                                         'password': "adminpass"}
        self.invalid_test_registration_data_last_name_greater_than_20 = {'first_name': "virat",
                                                                         'last_name': "kohlikohlikohlikohlikohli",
                                                                         'email': "viratkohli123@gmail.com",
                                                                         'user_name': "viratkohli",
                                                                         'password': "adminpass"}
        self.invalid_test_registration_data_user_name_not_alpha_numeric = {'first_name': "virat",
                                                                           'last_name': "kohlikohli",
                                                                           'email': "viratkohli123@gmail.com",
                                                                           'user_name': "viratkohli@123_",
                                                                           'password': "adminpass"}
        self.reset_password_url = reverse("request-reset-email")

        self.login_url = reverse("login")

        self.valid_login_data = {
            'email': "kamaltarun.rao0@gmail.com",
            'password': "adminpass"}
        self.valid_test_login_data = {'email': 'viratkohli123@gmail.com',
                                      'password': 'adminpass'}
        self.invalid_login_data = {
            'email': "kamaltarun.rao0@gmail.com",
            'password': "adminpa"}

        self.label_post_url = reverse("label-post")
        self.note_post_url = reverse("note")
        self.note_url = reverse("single-note", kwargs={"pk": 1})

        self.note_archived_url = reverse("archived")
        self.single_note_archived_url = reverse("single-archived", kwargs={"pk": 2})
        self.note_pinned_url = reverse("pinned")
        self.single_note_pinned_url = reverse("single-pinned", kwargs={"pk": 4})
        self.note_trash_url = reverse("trash")
        self.single_note_trash_url = reverse("single-trash", kwargs={"pk": 6})

        self.valid_label_data = {
            'label_name': "Third Note",
        }
        self.invalid_label_title_data = {
            'label_name': "notenotenotenotenotenotenotenotenotenotenotenotenotenotenotenotenotenotenotenotenotenotenote",
        }

        self.valid_note_data = {
            "title": "my testing note",
            "description": "this is my second note",
            "is_archived": True,
            "is_pinned": True,
            "label": ["Third Note"],
            "collaborate": ["kamaltarun.rao0@gmail.com"]
        }
        self.valid_note_data2 = {
            "title": "valid note",
            "description": "this is my valid note",
            "trash": True,
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
        self.search_note_url = reverse("search") + "?q=my second"
        self.empty_search_note_url = reverse("search") + "?q="
        self.label_url = 'http://127.0.0.1:8000/label/1'

        self.valid_label_put_data = {'label_name': "First Note",
                                     }
        self.invalid_label_data = {'label': "Third Note",
                                   }
        # self.client.post(self.register_url, self.valid_registration_data, format='json')
        # user = User.objects.filter(email=self.valid_registration_data['email']).first()
        # user.is_verified = True
        # user.save()
        #
        # self.logged_in = self.client.post(self.login_url, self.valid_login_data, format='json')


class RegistrationTests(Data):
    """
    this class will test registration view and match with status_code
    """

    def test_register_view_with_valid_details(self):
        """
        Ensure we can create a new account object and it returns status code as 201.
        """

        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.save()

        self.logged_in = self.client.post(self.login_url, self.valid_login_data, format='json')
        response = self.client.post(self.register_url, self.valid_test_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.save()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_view_with_password_missing(self):
        """
        Ensure we cannot create a new account object and returns status code as 400.
        """

        response = self.client.post(self.register_url, self.invalid_registration_data_password_missing, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_view_with_email_missing(self):
        """
        Ensure we cannot create a new account object and returns status code as 400.
        """

        response = self.client.post(self.register_url, self.invalid_registration_data_email_missing, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_view_with_email_length_greater_than_50(self):
        """
        Ensure we cannot create a new account object and returns status code as 400.
        """

        response = self.client.post(self.register_url, self.invalid_test_registration_data_email_length, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_view_with_password_length_less_than_6(self):
        """
        Ensure we cannot create a new account object and returns status code as 400.
        """

        response = self.client.post(self.register_url, self.invalid_test_registration_data_password_less_than_6,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_view_with_user_name_length_greater_than_20(self):
        """
        Ensure we cannot create a new account object and returns status code as 400.
        """

        response = self.client.post(self.register_url, self.invalid_test_registration_data_user_name_greater_than_20,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_view_with_last_name_length_greater_than_20(self):
        """
        Ensure we cannot create a new account object and returns status code as 400.
        """

        response = self.client.post(self.register_url, self.invalid_test_registration_data_last_name_greater_than_20,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_view_with_user_name_not_alpha_numeric(self):
        """
        Ensure we cannot create a new account object and returns status code as 400.
        """

        response = self.client.post(self.register_url, self.invalid_test_registration_data_user_name_not_alpha_numeric,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_password_reset_email(self):
        """
        Ensure we can reset password for email and it returns status code as 201.
        """
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.save()

        self.logged_in = self.client.post(self.login_url, self.valid_login_data, format='json')
        data = {"email": "kamaltarun.rao0@gmail.com"}
        response = self.client.post(self.reset_password_url, data, format='json')
        token = response.data['data']['email_body'].split(" ")[7]
        uidb64 = response.data['data']['email_body'].split(" ")[13]
        data = json.dumps({"password": "adminpass", "token": token, "uidb64": uidb64})

        response = self.client.patch(reverse("password-reset-complete"), data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        invalid_data = json.dumps({"password": "adminpass", "token": token, "uidb64": uidb64 + 's'})

        response = self.client.patch(reverse("password-reset-complete"), invalid_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {"email": "virat@gmail.com"}
        response = self.client.post(self.reset_password_url, data, format='json')
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
        response = self.client.post(self.login_url, self.invalid_login_data, format='json')
        assert response.status_code == 400

    def test_login_api_view_with_invalid_details_user_not_verified(self):
        """
        Ensure we cannot login and returns status code as 400.
        """

        self.client.post(self.register_url, self.valid_test_registration_data, format='json')
        response = self.client.post(self.login_url, self.valid_test_login_data, format='json')
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

        self.logged_in = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = self.logged_in.data['data']['token']

        response = self.client.post(self.label_post_url, self.valid_label_data, HTTP_AUTHORIZATION=headers,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(self.label_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.label_post_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.put(self.label_url, self.valid_label_put_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.put(self.label_url, self.invalid_label_title_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

        self.logged_in = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = self.logged_in.data['data']['token']

        response = self.client.post(self.label_post_url, self.invalid_label_data, HTTP_AUTHORIZATION=headers,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(self.label_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.put(self.label_url, self.valid_label_put_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.delete(self.label_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_labels_with_different_users_token(self):
        """
        Ensure we cannot login with other user's token.
        """
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.save()

        self.logged_in = self.client.post(self.login_url, self.valid_login_data, format='json')
        self.client.post(self.register_url, self.valid_test_registration_data, format='json')
        user = User.objects.filter(email=self.valid_test_registration_data['email']).first()
        user.is_verified = True
        user.save()

        headers = self.client.post(self.login_url, self.valid_login_data, format='json')
        self.client.post(self.label_post_url, self.valid_test_login_data, HTTP_AUTHORIZATION=headers,
                         format='json')
        headers = self.logged_in
        response = self.client.get(self.label_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class NotesTest(Data):
    """
    Test case for validating Notes class with valid and invalid details.
    """

    def test_notes_with_valid_details(self):
        """
        Test case for validating Labels class with valid details.
        """
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.save()

        self.logged_in = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = self.logged_in.data['data']['token']

        response = self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = client.post(self.note_post_url, self.valid_note_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = client.get(self.note_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = client.get(self.note_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = client.get(self.note_post_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.put(self.note_url, self.valid_note_put_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.delete(self.note_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_notes_with_invalid_details(self):
        """
        Test case for validating Labels class with invalid details.
        """
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.save()

        self.logged_in = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = self.logged_in.data['data']['token']

        response = self.client.post(self.note_post_url, self.invalid_note_data, HTTP_AUTHORIZATION=headers,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.get(self.note_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(self.note_url, self.valid_note_put_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.delete(self.note_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ArchivedViewTest(Data):
    """
    Test case for validating ArchivedViewTest class with valid and invalid details.
    """

    def test_archived_view_for_valid_details(self):
        """
        Test case for validating ArchivedView class with valid details.
        """
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.save()

        self.logged_in = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = self.logged_in.data['data']['token']
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
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.save()

        self.logged_in = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = self.logged_in.data['data']['token']
        self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data2, HTTP_AUTHORIZATION=headers, format='json')

        client.post(self.note_post_url, self.valid_note_data2, format='json')

        response = client.get(self.note_pinned_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get(self.single_note_pinned_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TrashViewTest(Data):

    def test_trash_view_for_valid_details(self):
        """
        Test case for validating TrashView class with valid details.
        """
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.save()

        self.logged_in = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = self.logged_in.data['data']['token']
        self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data2, HTTP_AUTHORIZATION=headers, format='json')

        response = self.client.get(self.note_trash_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.single_note_trash_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SearchNoteTest(Data):

    def test_search_note_for_valid_details(self):
        """
        Test case for validating SearchNote class with valid details.
        """
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.save()

        self.logged_in = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = self.logged_in.data['data']['token']
        self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data, HTTP_AUTHORIZATION=headers, format='json')
        response = client.get(self.search_note_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_note_with_no_details(self):
        """
        Test case for validating PinnedView class without providing details.
        """
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.save()

        self.logged_in = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = self.logged_in.data['data']['token']
        self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data, HTTP_AUTHORIZATION=headers, format='json')
        response = client.get(self.empty_search_note_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
