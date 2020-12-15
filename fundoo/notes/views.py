from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from fundooapp.models import Account
from .serializer import NoteSerializer
from .models import Note

User = get_user_model()


class AddNote(CreateAPIView):
    """
        This API is used to add notes.
        Parameter: (Title, Description, Color, etc.).
        CreateAPIView: Used for Create operations (Method-POST)
    """

    serializer_class = NoteSerializer

    def post(self, request, *args, **kwargs):
        try:
            res = {
                'message': 'Something bad happened',
                'status': status.HTTP_400_BAD_REQUEST
            }
            serializer = NoteSerializer(data=request.data)
            if request.data['title'] is None or request.data['description'] is None:
                res['message'] = "title and description required"
                return Response(res)

            if serializer.is_valid():
                serializer.save()
                res['message'] = "note added successfully"
                res['status'] = status.HTTP_201_CREATED
                return Response(res)
            res['message'] = "please enter valid data"
            return Response(res)
        except Exception as e:
            return Response(res)


class UpdateNote(UpdateAPIView):
    """
        This API is used to update notes.
        UpdateAPIView: Used for Update operations (Method-PUT)
    """
    serializer_class = NoteSerializer

    def put(self, request, *args, **kwargs):
        res = {
            'message': 'Something other issue',
            'status': status.HTTP_400_BAD_REQUEST
        }
        try:

            item = Note.objects.get(pk=kwargs.get('pk'))
            data = request.data
            serializer = NoteSerializer(item, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                res['message'] = "Update Successfully"
                res['status'] = status.HTTP_201_CREATED
                return Response(res)
            res['message'] = "please check the details entered"
            res['status'] = status.HTTP_400_BAD_REQUEST
            return Response(res)
        except Exception as e:
            res['message'] = e
            return Response(res)
