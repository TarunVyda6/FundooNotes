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
from services.exceptions import (MyCustomError, ExceptionType)
from services.cache import Cache
from services.encrypt import Encrypt

User = get_user_model()

logging.basicConfig(filename='notes.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')
cache = Cache()


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
            if 'title' not in data or data['title'] is '' or 'description' not in data or data['description'] is '':
                raise MyCustomError(ExceptionType.ValidationError, "title and description required")
            if serializer.is_valid():
                serializer.save()
                serialized_data = serializer.data
                return utils.manage_response(status=True, message='Note Added Successfully', data=serialized_data,
                                             status_code=status.HTTP_201_CREATED)
            raise MyCustomError(ExceptionType.LengthError, "title should be less than 150 characters")
        except MyCustomError as e:
            return utils.manage_response(status=False, message=e.message, exception=str(e),
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
                if cache.get_cache("NOTE_" + str(kwargs.get('pk')) + "_DETAIL") is not None:
                    notes = cache.get_cache("NOTE_" + str(kwargs.get('pk')) + "_DETAIL")
                    notes = Encrypt.decode(notes)
                else:
                    notes = Note.objects.filter(Q(pk=kwargs.get('pk')) &
                                                (Q(user=kwargs.get('user').id) | Q(
                                                    collaborate=kwargs.get('user').id))).exclude(trash=True).first()
                    if notes is None:
                        raise MyCustomError(ExceptionType.UnAuthorized, "note doesn't exist")
                    serializer = NoteSerializer(notes)
                    notes = serializer.data
                    cache_notes = Encrypt.encode(notes)
                    cache.set_cache("NOTE_" + str(kwargs.get('pk')) + "_DETAIL", cache_notes)
                return utils.manage_response(status=True, message="data retrieved successfully",
                                             data=notes,
                                             status_code=status.HTTP_200_OK)

            else:
                notes = Note.objects.filter(
                    Q(user=kwargs.get('user').id) | Q(collaborate=kwargs.get('user').id)).exclude(trash=True)
                serializer = NoteSerializer(notes, many=True)
                return utils.manage_response(status=True, message="data retrieved successfully",
                                             data=serializer.data,
                                             status_code=status.HTTP_200_OK)
        except MyCustomError as e:
            return utils.manage_response(status=False, message=e.message, exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)
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

            item = Note.objects.filter(Q(pk=kwargs.get('pk')) &
                                       (Q(user=kwargs.get('user').id) | Q(
                                           collaborate=kwargs.get('user').id))).exclude(trash=True).first()
            if item is None:
                raise MyCustomError(ExceptionType.UnAuthorized, "Note doesn't exist")
            data = request.data
            serializer = NoteSerializer(item, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                notes = serializer.data
                notes = Encrypt.encode(notes)
                cache.set_cache("NOTE_" + str(kwargs.get('pk')) + "_DETAIL", notes)
                return utils.manage_response(status=True, message="Note Update Successfully", data=serializer.data,
                                             status_code=status.HTTP_201_CREATED)
            raise MyCustomError(ExceptionType.ValidationError, "You have entered invalid details")

        except MyCustomError as e:
            return utils.manage_response(status=False, message=e.message, exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)
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
            note = Note.objects.filter(Q(pk=kwargs.get('pk')) &
                                       (Q(user=kwargs.get('user').id) | Q(
                                           collaborate=kwargs.get('user').id))).exclude(trash=True).first()
            if note is None:
                raise MyCustomError(ExceptionType.UnAuthorized, "Note doesn't exist")

            note.soft_delete()
            if cache.get_cache("NOTE_" + str(kwargs.get('pk')) + "_DETAIL") is not None:
                cache.delete_cache("NOTE_" + str(kwargs.get('pk')) + "_DETAIL")
            return utils.manage_response(status=True, message="Note Deleted Successfully",
                                         status_code=status.HTTP_202_ACCEPTED)

        except MyCustomError as e:
            return utils.manage_response(status=False, message=e.message, exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return utils.manage_response(status=False, message='some other issue please try after some time',
                                         exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)


@method_decorator(user_login_required, name="dispatch")
class ArchivedView(APIView):
    """
    this class will return all archived notes to which the user have permission to access
    """

    def get(self, request, *args, **kwargs):
        """
        this method takes pk from url in kwargs and return the particular archived note if exist. else it will return
        all archived notes of particular user
        :param kwargs: it takes primary key and user account object as input
        :return: all the request archived notes which user have requested
        """
        try:
            if kwargs.get('pk'):
                item = Note.objects.filter(Q(pk=kwargs.get('pk')) & Q(trash=False) & Q(is_archived=True) & (Q(
                    user=kwargs.get('user').id) | Q(
                    collaborate=kwargs.get('user').id))).first()
                if item is None:
                    raise MyCustomError(ExceptionType.UnAuthorized, "Note doesn't exist")
                serializer = NoteSerializer(item)
                return utils.manage_response(status=True, message="archived note retrieved successfully",
                                             data=serializer.data,
                                             status_code=status.HTTP_200_OK)

            else:
                item = Note.objects.filter(
                    (Q(user_id=kwargs.get('user').id) | Q(collaborate=kwargs.get('user').id)) & Q(
                        is_archived=True)).exclude(is_deleted=True)
                if item is None:
                    raise MyCustomError(ExceptionType.UnAuthorized, "Note doesn't exist")
                serializer = NoteSerializer(item, many=True)
                return utils.manage_response(status=True, message="archived notes retrieved successfully",
                                             data=serializer.data,
                                             status_code=status.HTTP_200_OK)
        except MyCustomError as e:
            return utils.manage_response(status=False, message=e.message, exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return utils.manage_response(status=False, message='some other issue please try after some time',
                                         exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)


@method_decorator(user_login_required, name="dispatch")
class PinnedView(APIView):
    """
    this class will return all pinned notes to which the user have permission to access
    """

    def get(self, request, *args, **kwargs):
        """
        this method takes pk from url in kwargs and return the particular pinned note if exist. else it will return
        all pinned notes of particular user
        :param kwargs: it takes primary key and user account object as input
        :return: all the request pinned notes which user have requested
        """
        try:
            if kwargs.get('pk'):
                item = Note.objects.filter(Q(pk=kwargs.get('pk')) & Q(trash=False) & Q(is_pinned=True) & (Q(
                    user=kwargs.get('user').id) | Q(
                    collaborate=kwargs.get('user').id))).first()
                if item is None:
                    raise MyCustomError(ExceptionType.UnAuthorized, "Note doesn't exist")
                serializer = NoteSerializer(item)
                return utils.manage_response(status=True, message="pinned note retrieved successfully",
                                             data=serializer.data,
                                             status_code=status.HTTP_200_OK)

            else:
                item = Note.objects.filter(
                    (Q(user_id=kwargs.get('user').id) | Q(collaborate=kwargs.get('user').id)) & Q(
                        is_pinned=True)).exclude(is_deleted=True)
                if item is None:
                    raise MyCustomError(ExceptionType.UnAuthorized, "Note doesn't exist")
                serializer = NoteSerializer(item, many=True)
                return utils.manage_response(status=True, message="pinned notes retrieved successfully",
                                             data=serializer.data,
                                             status_code=status.HTTP_200_OK)
        except MyCustomError as e:
            return utils.manage_response(status=False, message=e.message, exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return utils.manage_response(status=False, message='some other issue please try after some time',
                                         exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)


@method_decorator(user_login_required, name="dispatch")
class TrashView(APIView):
    """
    this class will return all trash notes to which the user have permission to access
    """

    def get(self, request, *args, **kwargs):
        """
        this method takes pk from url in kwargs and return the particular trash note if exist. else it will return
        all trash notes of particular user
        :param kwargs: it takes primary key and user account object as input
        :return: all the request trash notes which user have requested
        """
        try:
            if kwargs.get('pk'):
                item = Note.objects.filter(Q(pk=kwargs.get('pk')) & Q(is_deleted=False) & Q(trash=True) & (Q(
                    user=kwargs.get('user').id) | Q(
                    collaborate=kwargs.get('user').id))).first()
                if item is None:
                    raise MyCustomError(ExceptionType.UnAuthorized, "Note doesn't exist")
                serializer = NoteSerializer(item)
                return utils.manage_response(status=True, message="Trashed note retrieved successfully",
                                             data=serializer.data,
                                             status_code=status.HTTP_200_OK)

            else:
                item = Note.objects.filter(
                    (Q(user_id=kwargs.get('user').id) | Q(collaborate=kwargs.get('user').id)) & Q(
                        trash=True)).exclude(is_deleted=True)
                if item is None:
                    raise MyCustomError(ExceptionType.UnAuthorized, "Note doesn't exist")
                serializer = NoteSerializer(item, many=True)
                return utils.manage_response(status=True, message="Trashed notes retrieved successfully",
                                             data=serializer.data,
                                             status_code=status.HTTP_200_OK)
        except MyCustomError as e:
            return utils.manage_response(status=False, message=e.message, exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return utils.manage_response(status=False, message='some other issue please try after some time',
                                         exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)


@method_decorator(user_login_required, name='dispatch')
class SearchNote(APIView):
    """
    this class will return all requested search notes to which the user have permission to access
    """

    def get(self, request, **kwargs):
        """
        this method takes user id from kwargs and return all the search note if exist.
        :param kwargs: it takes user account object as input
        :return: all the notes which user have requested
        """
        try:
            current_user = kwargs.get('user').id
            search_terms = request.query_params.get('q')
            search_term_list = search_terms.split(' ')

            if search_terms == '':
                raise MyCustomError(ExceptionType.EmptyField, "please enter the note you want to search")

            notes = Note.objects.filter(Q(user=current_user) | Q(collaborate=current_user)).exclude(
                trash=True)

            search_query = Q(title__icontains=search_term_list[0]) | Q(description__icontains=search_term_list[0])

            for term in search_term_list[1:]:
                search_query.add((Q(title__icontains=term) | Q(description__icontains=term)),
                                 search_query.AND)

            notes = notes.filter(search_query)

            serializer = NoteSerializer(notes, many=True)
            return utils.manage_response(status=True, message='retrieved notes on the basis of search terms',
                                         data=serializer.data,
                                         status_code=status.HTTP_200_OK)
        except MyCustomError as e:
            return utils.manage_response(status=False, message=e.message, exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return utils.manage_response(status=False, message='some other issue please try after some time',
                                         exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)
