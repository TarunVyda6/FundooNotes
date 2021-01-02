from rest_framework.response import Response
import logging
from labels.models import *
from fundooapp.models import *


def set_user(request, user_id):
    """[sets user email to associated user id and modifies request.data]
    Args:
        request ([QueryDict]): [post data]
    Raises:
        Account.DoesNotExist: [if given email isn't found in database]
    """
    request.POST._mutable = True
    request.data["user"] = user_id
    request.POST._mutable = False


def get_collaborator_list(request):
    """[maps collaborator emails to their user ids and modifies request.data]

    Args:
        request ([QueryDict]): [post data]
    """
    request.POST._mutable = True
    collaborators_list = []  # holds ids associated to label names
    for collaborator_email in request.data.get('collaborate'):
        collab_qs = Account.objects.filter(email=collaborator_email)
        if not collab_qs:
            raise Account.DoesNotExist('No such user account exists')
        if collab_qs.exists() and collab_qs.count() == 1:
            collab_obj = collab_qs.first()  # assign object from queryset
            collaborators_list.append(collab_obj.id)  # append object id of the obtained object to list
    request.data["collaborate"] = collaborators_list
    request.POST._mutable = False


def get_label_list(request):
    """[maps label titles to their label ids and modifies request.data]

    Args:
        request ([QueryDict]): [post data]
    """
    request.POST._mutable = True
    label_list = []  # holds ids associated to label names
    for label_name in request.data.get('label'):
        label_qs = Label.objects.filter(label_name=label_name)
        if not label_qs:
            raise Label.DoesNotExist('No such label exists')
        if label_qs.exists() and label_qs.count() == 1:
            label_obj = label_qs.first()  # assign object from queryset
            label_list.append(label_obj.id)  # append object id of the obtained object to list
    request.data["label"] = label_list
    request.POST._mutable = False


def manage_response(**kwargs):
    """
    this function is used to log and return the responses
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


