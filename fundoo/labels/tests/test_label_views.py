from django.urls import reverse
from rest_framework import status
import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

client = APIClient()


@pytest.mark.django_db()
class Data(TestCase):
    """
    this class will initialise all the urls and data and it is inherited by other test classes
    """

    def setUp(self):
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
        self.valid_label_data = {
            'label_name': "Third Note",
        }
        self.valid_test_login_data = {'email': 'viratkohli123@gmail.com',
                                      'password': 'adminpass'}
        self.valid_label_put_data = {'label_name': "First Note",
                                     }
        self.invalid_label_data = {'label': "Third Note",
                                   }
        self.invalid_label_title_data = {
            'label_name': "notenotenotenotenotenotenotenotenotenotenotenotenotenotenotenotenotenotenotenotenotenotenote",
        }
        self.label_url = reverse('label', kwargs={'pk': 2})
        self.label_post_url = reverse("label-post")


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
        self.headers = self.logged_in.__getitem__("HTTP_AUTHORIZATION")

        response = self.client.post(self.label_post_url, self.valid_label_data, HTTP_AUTHORIZATION=self.headers,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(self.label_url, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.label_post_url, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.put(self.label_url, self.valid_label_put_data, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.put(self.label_url, self.invalid_label_title_data, HTTP_AUTHORIZATION=self.headers,
                              format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.delete(self.label_url, HTTP_AUTHORIZATION=self.headers, format='json')
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
        self.headers = self.logged_in.__getitem__("HTTP_AUTHORIZATION")

        response = self.client.post(self.label_post_url, self.invalid_label_data, HTTP_AUTHORIZATION=self.headers,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(self.label_url, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.put(self.label_url, self.valid_label_put_data, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.delete(self.label_url, HTTP_AUTHORIZATION=self.headers, format='json')
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
        self.headers = self.logged_in.__getitem__("HTTP_AUTHORIZATION")

        self.client.post(self.register_url, self.valid_test_registration_data, format='json')
        user = User.objects.filter(email=self.valid_test_registration_data['email']).first()
        user.is_verified = True
        user.save()
        logged = self.client.post(self.login_url, self.valid_login_data, format='json')
        logged_token = logged.__getitem__("HTTP_AUTHORIZATION")
        self.client.post(self.label_post_url, self.valid_test_login_data, HTTP_AUTHORIZATION=logged_token,
                         format='json')
        response = self.client.get(self.label_url, HTTP_AUTHORIZATION=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
