from rest_framework.response import Response
from rest_framework import status
from .serializer import LabelSerializer
from .models import Label
from rest_framework.views import APIView
import logging
from notes import utils
from django.utils.decorators import method_decorator
from fundooapp.decorator import user_login_required
import json

logging.basicConfig(filename='labels.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


@method_decorator(user_login_required, name="dispatch")
class Labels(APIView):
    """
    Label class is used to perform CRUD operations on labels and it stores the data in database
    :rtype:Response returns success or failure message along with status
    """
    serializer_class = LabelSerializer

    def post(self, request, *args, **kwargs):
        """
        takes label data as input and if the data is valid then it stores the data in database
        :rtype:Response returns success or failure message along with status
        """

        try:
            _mutable = request.data._mutable
            request.data._mutable = True
            request.data['user'] = str(kwargs.get('user').id)
            request.data._mutable = _mutable
            serializer = LabelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return utils.manage_response(status=True, message='Label Added Successfully', data=serializer.data,
                                             status_code=status.HTTP_201_CREATED)
            return utils.manage_response(status=False, message='maximum length of label name should be 50 characters',
                                         status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return utils.manage_response(status=False, message='some other issue please try after some time',
                                         exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)

    def get(self, *args, **kwargs):
        """
        takes key as input and if data exists for that key then it returns the data from database
        :rtype:Response returns data along if it is success else returns failure message along with status
        """

        try:

            if kwargs.get('pk'):
                item = Label.objects.get(pk=kwargs.get('pk'), is_deleted=False)
                if item.user == kwargs.get('user'):
                    serializer = LabelSerializer(item)
                    return utils.manage_response(status=True, message="Label retrieved successfully",
                                                 data=serializer.data,
                                                 status_code=status.HTTP_200_OK)
                else:
                    return utils.manage_response(status=False,
                                                 message="you don't have permission to retrieve this label",
                                                 status_code=status.HTTP_401_UNAUTHORIZED)
            else:
                labels = Label.objects.filter(user_id=kwargs.get('user').id, is_deleted=False)
                serializer = LabelSerializer(labels, many=True)
                return utils.manage_response(status=True, message="Labels retrieved successfully",
                                             data=serializer.data,
                                             status_code=status.HTTP_200_OK)

        except Label.DoesNotExist:
            return utils.manage_response(status=False, message="Please enter valid label id",
                                         status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return utils.manage_response(status=False, message='some other issue please try after some time',
                                         exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        """
        takes label data as input and if the data is valid then it replaces the data in database
        :rtype:Response returns success or failure message along with status
        """

        try:

            item = Label.objects.get(pk=kwargs.get('pk'), is_deleted=False)
            if item.user == kwargs.get('user'):
                serializer = LabelSerializer(item, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return utils.manage_response(status=True, message="Label Update Successfully", data=serializer.data,
                                                 status_code=status.HTTP_201_CREATED)
                return utils.manage_response(status=False,
                                             message="maximum length of label name should be 50 characters",
                                             status_code=status.HTTP_400_BAD_REQUEST)
            else:
                return utils.manage_response(status=False,
                                             message="you don't have permission to update this label",
                                             status_code=status.HTTP_401_UNAUTHORIZED)

        except Label.DoesNotExist:
            return utils.manage_response(status=False, message="Please enter valid label id",
                                         status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return utils.manage_response(status=False, message='some other issue please try after some time',
                                         exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        """
        takes key as input and if data exists for that key then it returns the delete that data from database
        :rtype:Response returns success or failure message along with status
        """

        try:
            item = Label.objects.get(id=kwargs.get('pk'), is_deleted=False)
            if item.user == kwargs.get('user'):
                item.soft_delete()
                return utils.manage_response(status=True, message="Label Deleted Successfully",
                                             status_code=status.HTTP_202_ACCEPTED)
            else:
                return utils.manage_response(status=False,
                                             message="you don't have permission to delete this label",
                                             status_code=status.HTTP_401_UNAUTHORIZED)

        except Label.DoesNotExist:
            return utils.manage_response(status=False, message="Please enter valid label id",
                                         status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return utils.manage_response(status=False, message='some other issue please try after some time',
                                         exception=str(e),
                                         status_code=status.HTTP_400_BAD_REQUEST)
