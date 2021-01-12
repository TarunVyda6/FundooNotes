from rest_framework.response import Response
import logging
from labels.models import *
from fundooapp.models import *
from services.exceptions import *


def set_user(request, user_id):
    """
        takes request and user id as input and sets user id to request user id
    """
    request.POST._mutable = True
    request.data["user"] = user_id
    request.POST._mutable = False


def get_collaborator_list(request):
    """
        takes request as input and return collaborate user id list
    """
    request.POST._mutable = True
    collaborators_list = []  # holds ids associated to label names
    collabs = request.data['collaborate']
    for collaborator_email in collabs:
        collab_qs = Account.objects.filter(email=collaborator_email)
        if not collab_qs:
            raise MyCustomError(ExceptionType.ValidationError, "No such user account exists")
        if collab_qs.exists() and collab_qs.count() == 1:
            collab_obj = collab_qs.first()  # assign object from queryset
            collaborators_list.append(collab_obj.id)  # append object id of the obtained object to list

    request.data["collaborate"] = collaborators_list
    request.POST._mutable = False


def get_label_list(request):
    """
        takes request as input and return label list
    """
    request.POST._mutable = True
    label_list = []  # holds ids associated to label names
    if not request.POST.getlist('label'):
        labels = request.data['label']
    else:
        labels = request.POST.getlist('label')
    for label_name in labels:
        label_qs = Label.objects.filter(label_name=label_name)
        if not label_qs:
            raise MyCustomError(ExceptionType.ValidationError, "No such label exists")
        if label_qs.exists() and label_qs.count() == 1:
            label_obj = label_qs.first()  # assign object from queryset
            label_list.append(label_obj.id)  # append object id of the obtained object to list
    request.data["label"] = label_list
    request.POST._mutable = False


def manage_response(**kwargs):
    """
    this function takes
    status : if the code executes without exception this will take False and returns False statement, else returns True
    message : this argument takes success of failed message and returns in response
    status_code : it will take success or failed or exception status_code and returns in response
    exception : if there is any exception occurs then this will carry that exception message and stores it in log file
    """
    result = {'status': kwargs['status'], 'message': kwargs['message'], 'status_code': kwargs['status_code']}
    if 'exception' in kwargs:
        logging.debug('{}, status_code = {}, exception = {}'.format(result, kwargs['status_code'], kwargs['exception']))
    elif 'data' in kwargs:
        result['data'] = kwargs['data']
        logging.debug(
            '{}, status_code = {} '.format(result, kwargs['status_code']))
        return Response(result, kwargs['status_code'])
    else:
        logging.debug('{}, status_code = {} '.format(result, kwargs['status_code']))
    return Response(result, kwargs['status_code'])
