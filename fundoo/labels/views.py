from rest_framework.response import Response
from rest_framework import status
from .serializer import LabelSerializer
from .models import Label
from rest_framework.views import APIView
import logging

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
                res['message'] = "Label Added Successfully"
                res['status'] = True
                logging.debug('{}'.format(res))
                return Response(res)
            res['message'] = "maximum length of label name should be 50 characters"
            logging.debug('{}'.format(res))
            return Response(res, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            res['message'] = str(e)
            logging.debug('{}'.format(res))
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
            res['message'] = serializer.data
            res['status'] = True
            logging.debug('{}'.format(res))
            return Response(res, status.HTTP_200_OK)
        except Label.DoesNotExist:
            res['message'] = "The requested label doesn't exist"
            return Response(res, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            res['message'] = str(e)
            logging.debug('{}'.format(res))
            return Response(res, status.HTTP_400_BAD_REQUEST)

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
                res['message'] = "Label Update Successfully"
                res['status'] = True
                logging.debug('{}'.format(res))
                return Response(res, status.HTTP_201_CREATED)
            res['message'] = "maximum length of label name should be 50 characters"
            res['status'] = False
            logging.debug('{}'.format(res))
            return Response(res, status.HTTP_400_BAD_REQUEST)
        except Label.DoesNotExist:
            res['message'] = "The requested label doesn't exist"
            return Response(res, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            res['message'] = str(e)
            logging.debug('{}'.format(res))
            return Response(res, status.HTTP_400_BAD_REQUEST)

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
            res['message'] = 'Label Deleted Successfully'
            res['status'] = True
            logging.debug('{}'.format(res))
            return Response(res, status.HTTP_202_ACCEPTED)
        except Label.DoesNotExist:
            res['message'] = "The requested label doesn't exist"
            return Response(res, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            res['message'] = str(e)
            logging.debug('{}'.format(res))
            return Response(res, status.HTTP_404_NOT_FOUND)
