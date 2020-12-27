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


@method_decorator(user_login_required, name="dispatch")
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

        try:

            serializer = LabelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return utils.manage_response(status=True, message='Label Added Successfully',
                                             status_code=status.HTTP_201_CREATED)
            return utils.manage_response(status=False, message='maximum length of label name should be 50 characters',
                                         status_code=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return utils.manage_response(status=False, message='some other issue please try after some time',
                                         status_code=status.HTTP_400_BAD_REQUEST)

    def get(self, *args, **kwargs):
        """
        takes key as input and if data exists for that key then it returns the data from database
        :rtype:Response returns data along if it is success else returns failure message along with status
        """

        try:
            item = Label.objects.get(pk=kwargs.get('pk'), is_deleted=False)
            serializer = LabelSerializer(item)
            return utils.manage_response(status=True, message=serializer.data, status_code=status.HTTP_200_OK)

        except Label.DoesNotExist:
            return utils.manage_response(status=False, message="Please enter valid label id",
                                         status_code=status.HTTP_404_NOT_FOUND)
        except Exception:
            return utils.manage_response(status=False, message='some other issue please try after some time',
                                         status_code=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        """
        takes label data as input and if the data is valid then it replaces the data in database
        :rtype:Response returns success or failure message along with status
        """

        try:

            item = Label.objects.get(pk=kwargs.get('pk'), is_deleted=False)
            serializer = LabelSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return utils.manage_response(status=True, message="Label Update Successfully",
                                             status_code=status.HTTP_201_CREATED)
            return utils.manage_response(status=False, message="maximum length of label name should be 50 characters",
                                         status_code=status.HTTP_400_BAD_REQUEST)
        except Label.DoesNotExist:
            return utils.manage_response(status=False, message="Please enter valid label id",
                                         status_code=status.HTTP_404_NOT_FOUND)
        except Exception:
            return utils.manage_response(status=False, message='some other issue please try after some time',
                                         status_code=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        """
        takes key as input and if data exists for that key then it returns the delete that data from database
        :rtype:Response returns success or failure message along with status
        """

        try:
            label = Label.objects.get(id=kwargs.get('pk'), is_deleted=False)
            label.soft_delete()
            return utils.manage_response(status=True, message="Label Deleted Successfully",
                                         status_code=status.HTTP_202_ACCEPTED)
        except Label.DoesNotExist:
            return utils.manage_response(status=False, message="Please enter valid label id",
                                         status_code=status.HTTP_404_NOT_FOUND)
        except Exception:
            return utils.manage_response(status=False, message='some other issue please try after some time',
                                         status_code=status.HTTP_400_BAD_REQUEST)
