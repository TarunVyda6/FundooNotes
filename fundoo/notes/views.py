from django.contrib.auth import get_user_model
from rest_framework import status
from .serializer import NoteSerializer
from .models import Note
from rest_framework.views import APIView
from . import utils
import logging
from django.utils.decorators import method_decorator
from fundooapp.decorator import user_login_required
from django.db.models import Q

User = get_user_model()

logging.basicConfig(filename='notes.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


@method_decorator(user_login_required, name="dispatch")
class Notes(APIView):
    """
    Notes class is used to perform CRUD operations on note and it stores the data in database
    :rtype:Response returns success or failure message along with status
    """
    serializer_class = NoteSerializer

    def post(self, request, *args, **kwargs):
        """
        takes notes data as input and if the data is valid then it stores the data in database
        :rtype:Response returns success or failure message along with statuscode
        """

        try:
            utils.set_user(request, kwargs.get('user').id)
            if request.data.get('collaborate'):
                utils.get_collaborator_list(request)
            if request.data.get('label'):
                utils.get_label_list(request)
            data = request.data
            serializer = NoteSerializer(data=data)
            if data['title'] is None or data['description'] is None:
                return utils.manage_response(status=False, message='title and description required',
                                             status_code=status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                serializer.save()
                return utils.manage_response(status=True, message='Note Added Successfully', data=serializer.data,
                                             status_code=status.HTTP_201_CREATED)
            return utils.manage_response(status=False, message='title should be less than 150 characters',
                                         status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return utils.manage_response(status=False, message='some other issue please try after some time',
                                         exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """
        takes key as input and if the data is exists in database then the data is returned
        :rtype:Response returns data if success else returns failure message along with statuscode
        """

        try:
            if kwargs.get('pk'):
                item = Note.objects.get(pk=kwargs.get('pk'), is_deleted=False)
                collaborators = item.collaborate.all()
                collaborator_list = list(map(lambda items: items.id, collaborators))
                if kwargs.get('user').id in collaborator_list:
                    serializer = NoteSerializer(item)

                    return utils.manage_response(status=True, message="data retrieved successfully",
                                                 data=serializer.data,
                                                 status_code=status.HTTP_200_OK)
                else:
                    return utils.manage_response(status=False,
                                                 message="you don't have permission to retrieve this note",
                                                 status_code=status.HTTP_401_UNAUTHORIZED)
            else:
                notes = Note.objects.filter(
                    Q(user=kwargs.get('user').id) | Q(collaborate=kwargs.get('user').id)).exclude(is_deleted=True)
                serializer = NoteSerializer(notes, many=True)
                return utils.manage_response(status=True, message="data retrieved successfully",
                                             data=serializer.data,
                                             status_code=status.HTTP_200_OK)
        except Note.DoesNotExist:
            return utils.manage_response(status=False, message="Please enter valid Note id",
                                         status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return utils.manage_response(status=False, message='some other issue please try after some time',
                                         exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        """
        takes key as input and if the data is valid then it replaces data in database
        :rtype:Response returns data if success else returns failure message along with statuscode
        """

        try:

            item = Note.objects.get(pk=kwargs.get('pk'), is_deleted=False)
            collaborators = item.collaborate.all()
            collaborator_list = list(map(lambda items: items.id, collaborators))
            if kwargs.get('user').id in collaborator_list:
                data = request.data
                serializer = NoteSerializer(item, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return utils.manage_response(status=True, message="Note Update Successfully", data=serializer.data,
                                                 status_code=status.HTTP_201_CREATED)
                return utils.manage_response(status=False, message="You have entered invalid details",
                                             status_code=status.HTTP_400_BAD_REQUEST)
            else:
                return utils.manage_response(status=False,
                                             message="you don't have permission to update this note",
                                             status_code=status.HTTP_401_UNAUTHORIZED)
        except Note.DoesNotExist:
            return utils.manage_response(status=False, message="Please enter valid Note id",
                                         status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return utils.manage_response(status=False, message='some other issue please try after some time',
                                         exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        takes key as input and if the data is exists in database then the it deletes the data from database
        :rtype:Response returns success else or failure message along with statuscode
        """

        try:
            note = Note.objects.get(id=kwargs.get('pk'), is_deleted=False)
            collaborators = note.collaborate.all()
            collaborator_list = list(map(lambda items: items.id, collaborators))
            if kwargs.get('user').id in collaborator_list:
                note.soft_delete()
                return utils.manage_response(status=True, message="Note Deleted Successfully",
                                             status_code=status.HTTP_202_ACCEPTED)
            else:
                return utils.manage_response(status=False,
                                             message="you don't have permission to delete this note",
                                             status_code=status.HTTP_401_UNAUTHORIZED)
        except Note.DoesNotExist:
            return utils.manage_response(status=False, message="Please enter valid Note id",
                                         status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return utils.manage_response(status=False, message='some other issue please try after some time',
                                         exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)
