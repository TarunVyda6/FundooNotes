from rest_framework import status
from rest_framework.test import APITestCase


class Data(APITestCase):
    def setUp(self):
        self.register_url = 'http://127.0.0.1:8000/register/'
        self.label_post_url = 'http://127.0.0.1:8000/label/'
        self.label_url = 'http://127.0.0.1:8000/label/1'

        self.valid_label_data = {'user': 1,
                                 'label_name': "Third Note",
                                 }
        self.valid_label_put_data = {'user': 1,
                                     'label': "First Note",
                                     }
        self.invalid_label_data = {'user': 15,
                                   'label': "Third Note",
                                   }
        self.valid_registration_data = {'first_name': "tarun",
                                        'last_name': "vyda",
                                        'email': "kamaltarun.rao0@gmail.com",
                                        'user_name': "tarunvyda",
                                        'password': "adminpass"}


class NotesTest(Data):

    def test_given_valid_label_details_for_crud(self):
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        self.client.post(self.label_post_url, self.valid_label_data, format='json')

        response = self.client.get(self.label_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(self.label_url, self.valid_label_put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete(self.label_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_given_invalid_label_details_for_crud(self):
        response = self.client.post(self.label_post_url, self.invalid_label_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(self.label_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(self.label_url, self.valid_label_put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.delete(self.label_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
