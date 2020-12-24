from rest_framework.response import Response
from rest_framework import status
from .serializer import LabelSerializer
from .models import Label
from rest_framework.views import APIView
import logging
from notes import utils
from django.utils.decorators import method_decorator
from fundooapp.decorator import user_login_required

logging.basicConfig(filename='labels.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class Labels(APIView):
    """
    Label class is used to perform CRUD operations on labels and it stores the data in database
    :rtype:Response returns success or failure message along with status
    """
    serializer_class = LabelSerializer

    def post(self, request):
        """
        takes label data as input and if the data is valid then it stores the data in database
        :rtype:Response returns success or failure message along with status
        """
        res = {
            'message': 'Something other issue',
            'status': False
        }
        try:

            serializer = LabelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                result = utils.manage_response(status=True, message='Label Added Successfully')
                logging.debug('{}'.format(result))
                return Response(result)
            result = utils.manage_response(status=False, message='maximum length of label name should be 50 characters')
            logging.debug('{}'.format(result))
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.debug('{}'.format(result))
            return Response(res, status.HTTP_400_BAD_REQUEST)

    def get(self, *args, **kwargs):
        """
        takes key as input and if data exists for that key then it returns the data from database
        :rtype:Response returns data along if it is success else returns failure message along with status
        """
        res = {
            'message': 'Something other issue',
            'status': False
        }
        try:
            item = Label.objects.get(pk=kwargs.get('pk'), is_deleted=False)
            serializer = LabelSerializer(item)
            result = utils.manage_response(status=True, message=serializer.data)
            logging.debug('{}'.format(result))
            return Response(result, status.HTTP_200_OK)
        except Label.DoesNotExist:
            result = utils.manage_response(status=False, message="Please enter valid label id")
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result = utils.manage_response(status=False, message='some other issue please try after some time')
            logging.debug('{}'.format(result))
            return Response(result, status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        """
        takes label data as input and if the data is valid then it replaces the data in database
        :rtype:Response returns success or failure message along with status
        """
        res = {
            'message': 'Something other issue',
            'status': False
        }
        try:

            item = Label.objects.get(pk=kwargs.get('pk'), is_deleted=False)
            serializer = LabelSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                result = utils.manage_response(status=True, message="Label Update Successfully")
                logging.debug('{}'.format(result))
                return Response(result, status.HTTP_201_CREATED)
            result = utils.manage_response(status=False, message="maximum length of label name should be 50 characters")
            logging.debug('{}'.format(result))
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Label.DoesNotExist:
            result = utils.manage_response(status=False, message="Please enter valid label id")
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result = utils.manage_response(status=False, message="Some other issue. Please try after some time")
            logging.debug('{}'.format(result))
            return Response(result, status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        """
        takes key as input and if data exists for that key then it returns the delete that data from database
        :rtype:Response returns success or failure message along with status
        """
        res = {
            'message': 'Some other issue',
            'status': False
        }
        try:
            label = Label.objects.get(id=kwargs.get('pk'), is_deleted=False)
            label.soft_delete()
            result = utils.manage_response(status=True, message="Note deleted successfully")
            logging.debug('{}'.format(result))
            return Response(result, status.HTTP_202_ACCEPTED)
        except Label.DoesNotExist:
            result = utils.manage_response(status=False, message="Please enter valid label id")
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result = utils.manage_response(status=False, message="Some other issue. Please try after some time")
            logging.debug('{}'.format(result))
            return Response(result, status.HTTP_404_NOT_FOUND)
