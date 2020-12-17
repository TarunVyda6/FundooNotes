from rest_framework.response import Response
from rest_framework import status
from .serializer import LabelSerializer
from .models import Label
from rest_framework.views import APIView


class Labels(APIView):
    serializer_class = LabelSerializer

    def post(self, request):
        res = {
            'message': 'Something bad happened',
            'status': False
        }
        try:

            serializer = LabelSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                res['message'] = "Label Added Successfully"
                res['status'] = True
                return Response(res)
            res['message'] = "please enter valid data"
            return Response(res, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            res['message'] = str(e)
            return Response(res, status.HTTP_400_BAD_REQUEST)

    def get(self, *args, **kwargs):
        res = {
            'message': 'Something other issue',
            'status': False
        }
        try:
            item = Label.objects.get(pk=kwargs.get('pk'))
            serializer = LabelSerializer(item)
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

            item = Label.objects.get(pk=kwargs.get('pk'))
            data = request.data
            serializer = LabelSerializer(item, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                res['message'] = "Label Update Successfully"
                res['status'] = True
                return Response(res, status.HTTP_201_CREATED)
            res['message'] = "please check the details entered"
            res['status'] = False
            return Response(res, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            res['message'] = str(e)
            return Response(res, status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        res = {
            'message': 'Some other issue',
            'status': False
        }
        try:
            note = Label.objects.get(id=kwargs.get('pk'))
            note.delete()
            res['message'] = 'Label Deleted Successfully'
            res['status'] = True
            return Response(res, status.HTTP_202_ACCEPTED)

        except Exception as e:
            res['message'] = str(e)
            return Response(res, status.HTTP_404_NOT_FOUND)
