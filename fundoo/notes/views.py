from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from .serializer import NoteSerializer
from .models import Note
from rest_framework.views import APIView
from . import utils
import logging
from django.utils.decorators import method_decorator
from fundooapp.decorator import user_login_required

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
                result = utils.manage_response(status=False, message='title and description required')
                logging.debug('{}'.format(result))
                return Response(result, status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                serializer.save()
                result = utils.manage_response(status=True, message='Note Added Successfully')
                logging.debug('{}'.format(result))
                return Response(result, status.HTTP_201_CREATED)
            result = utils.manage_response(status=False, message='title should be less than 150 characters')
            logging.debug('{}'.format(result))
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result = utils.manage_response(status=False, message='some other issue occured please try after some time')
            logging.debug('{}'.format(result))
            return Response(result, status.HTTP_400_BAD_REQUEST)

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
            result = utils.manage_response(status=True, message=serializer.data)
            logging.debug('{}'.format(result))
            return Response(result, status.HTTP_200_OK)
        except Note.DoesNotExist:
            result = utils.manage_response(status=False, message="Please enter valid note id")
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result = utils.manage_response(status=False, message='some other issue please try after some time')
            logging.debug('{}'.format(result))
            return Response(result, status.HTTP_400_BAD_REQUEST)

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
                result = utils.manage_response(status=True, message="Note Update Successfully")
                logging.debug('{}'.format(result))
                return Response(res, status.HTTP_201_CREATED)
            result = utils.manage_response(status=False, message="You have entered invalid details")
            logging.debug('{}'.format(result))
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Note.DoesNotExist:
            result = utils.manage_response(status=False, message="Please enter valid note id")
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result = utils.manage_response(status=False, message="Some other issue. Please try after some time")
            logging.debug('{}'.format(result))
            return Response(result, status.HTTP_400_BAD_REQUEST)

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
            result = utils.manage_response(status=True, message="Note deleted successfully")
            logging.debug('{}'.format(result))
            return Response(res, status.HTTP_202_ACCEPTED)
        except Note.DoesNotExist:
            result = utils.manage_response(status=False, message="Please enter valid note id")
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result = utils.manage_response(status=False, message="Some other issue. Please try after some time")
            logging.debug('{}'.format(result))
            return Response(result, status.HTTP_404_NOT_FOUND)
