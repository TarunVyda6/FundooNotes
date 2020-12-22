from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class Data(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.note_post_url = reverse("note")
        self.note_url = 'http://127.0.0.1:8000/note/1'
        self.label_url = reverse("label-post")

        self.valid_label_data = {'user': 1,
                                 'label_name': "Third Note",
                                 }

        self.valid_note_data = {"user": "viratkohli123@gmail.com",
                                "title": "my testing note",
                                "description": "this is my second note",
                                "label": ["Third Note"],
                                "collaborate": ["viratkohli123@gmail.com"]
                                }
        self.valid_note_put_data = {
            "title": "testing note",
            "description": "this is changed note",
        }
        self.invalid_note_data = {'user': "viratkohli123@gmail.com",
                                  'description': "this is my second note",
                                  'label': "Third Note",
                                  'collaborate': ["viratkohli123@gmail.com"],
                                  }
        self.valid_registration_data = {'first_name': "tarun",
                                        'last_name': "vyda",
                                        'email': "viratkohli123@gmail.com",
                                        'user_name': "tarunvyda",
                                        'password': "adminpass"}


class NotesTest(Data):

    def test_given_valid_note_url_for_crud(self):
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        self.client.post(self.label_url, self.valid_label_data, format='json')
        self.client.post(self.note_post_url, self.valid_note_data, format='json')

        response = self.client.get(self.note_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(self.note_url, self.valid_note_put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete(self.note_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_given_invalid_note_details_for_crud(self):
        response = self.client.post(self.note_post_url, self.invalid_note_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(self.note_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(self.note_url, self.valid_note_put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.delete(self.note_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
