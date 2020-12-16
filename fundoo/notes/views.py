from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from .serializer import NoteSerializer
from .models import Note
from rest_framework.views import APIView

User = get_user_model()


class Notes(APIView):
    serializer_class = NoteSerializer

    def post(self, request):
        res = {
            'message': 'Something bad happened',
            'status': False
        }
        try:

            serializer = NoteSerializer(data=request.data)
            if request.data['title'] is None or request.data['description'] is None:
                res['message'] = "title and description required"
                return Response(res, status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                serializer.save()
                res['message'] = "Note Added Successfully"
                res['status'] = True
                return Response(res)
            res['message'] = "please enter valid data"
            return Response(res, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            res['message'] = str(e)
            return Response(res, status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        res = {
            'message': 'Something other issue',
            'status': False
        }
        try:
            item = Note.objects.get(pk=kwargs.get('pk'))
            serializer = NoteSerializer(item)
            res['message'] = serializer.data
            res['status'] = True
            return Response(res, status.HTTP_200_OK)
        except Exception as e:
            res['message'] = str(e)
            return Response(res, status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        res = {
            'message': 'Something other issue',
            'status': False
        }
        try:

            item = Note.objects.get(pk=kwargs.get('pk'))
            data = request.data
            serializer = NoteSerializer(item, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                res['message'] = "Note Update Successfully"
                res['status'] = True
                return Response(res, status.HTTP_201_CREATED)
            res['message'] = "please check the details entered"
            res['status'] = False
            return Response(res, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            res['message'] = str(e)
            return Response(res, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        res = {
            'message': 'Some other issue',
            'status': False
        }
        try:
            note = Note.objects.get(id=kwargs.get('pk'))
            note.delete()
            res['message'] = 'Note Deleted Successfully'
            res['status'] = True
            return Response(res, status.HTTP_202_ACCEPTED)

        except Exception as e:
            res['message'] = str(e)
            return Response(res, status.HTTP_404_NOT_FOUND)
