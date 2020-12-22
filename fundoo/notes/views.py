from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from .serializer import NoteSerializer
from .models import Note
from rest_framework.views import APIView
from . import utils
import logging

User = get_user_model()

logging.basicConfig(filename='notes.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class Notes(APIView):
    """
        Notes class is used to perform CRUD operations on note and it stores the data in database
        :rtype:Response returns success or failure message along with status
        """
    serializer_class = NoteSerializer

    def post(self, request):
        """
        takes notes data as input and if the data is valid then it stores the data in database
        :rtype:Response returns success or failure message along with statuscode
        """
        res = {
            'message': 'Something bad happened',
            'status': False
        }
        try:

            if request.data.get('user'):
                utils.get_user(request)

            if request.data.get('collaborate'):
                utils.get_collaborator_list(request)
            if request.data.get('label'):
                utils.get_label_list(request)
            data = request.data
            serializer = NoteSerializer(data=data)
            if data['title'] is None or data['description'] is None:
                res['message'] = "title and description required"
                logging.debug('{}'.format(res))
                return Response(res, status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                serializer.save()
                res['message'] = "Note Added Successfully"
                res['status'] = True
                logging.debug('{}'.format(res))
                return Response(res, status.HTTP_201_CREATED)
            res['message'] = "title should be less than 150 characters"
            logging.debug('{}'.format(res))
            return Response(res, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            res['message'] = str(e)
            logging.debug('{}'.format(res))
            return Response(res, status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """
        takes key as input and if the data is exists in database then the data is returned
        :rtype:Response returns data if success else returns failure message along with statuscode
        """
        res = {
            'message': 'Something other issue',
            'status': False
        }
        try:
            item = Note.objects.get(pk=kwargs.get('pk'), is_deleted=False)
            serializer = NoteSerializer(item)
            res['message'] = serializer.data
            res['status'] = True
            logging.debug('{}'.format(res))
            return Response(res, status.HTTP_200_OK)
        except Note.DoesNotExist:
            res['message'] = "The requested note doesn't exist"
            return Response(res, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            res['message'] = str(e)
            logging.debug('{}'.format(res))
            return Response(res, status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        """
        takes key as input and if the data is valid then it replaces data in database
        :rtype:Response returns data if success else returns failure message along with statuscode
        """
        res = {
            'message': 'Something other issue',
            'status': False
        }
        try:

            item = Note.objects.get(pk=kwargs.get('pk'), is_deleted=False)
            data = request.data
            serializer = NoteSerializer(item, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                res['message'] = "Note Update Successfully"
                res['status'] = True
                logging.debug('{}'.format(res))
                return Response(res, status.HTTP_201_CREATED)
            res['message'] = "please check the details entered"
            res['status'] = False
            logging.debug('{}'.format(res))
            return Response(res, status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            res['message'] = str(e)
            logging.debug('{}'.format(res))
            return Response(res, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        takes key as input and if the data is exists in database then the it deletes the data from database
        :rtype:Response returns success else or failure message along with statuscode
        """
        res = {
            'message': 'Some other issue',
            'status': False
        }
        try:
            note = Note.objects.get(id=kwargs.get('pk'), is_deleted=False)
            note.soft_delete()
            res['message'] = 'Note Deleted Successfully'
            res['status'] = True
            logging.debug('{}'.format(res))
            return Response(res, status.HTTP_202_ACCEPTED)
        except Note.DoesNotExist:
            res['message'] = "The requested note doesn't exist"
        except Exception as e:
            res['message'] = str(e)
            logging.debug('{}'.format(res))
            return Response(res, status.HTTP_404_NOT_FOUND)