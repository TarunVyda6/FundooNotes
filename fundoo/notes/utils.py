"""
Overview: contains logic for converting emails or label names to ids in request.data
Author: Anam Fazal
Created on: Dec 18, 2020
"""
from labels.models import Label
from fundooapp.models import Account


def get_user(request):
    """[sets user email to associated user id and modifies request.data]
    Args:
        request ([QueryDict]): [post data]
    Raises:
        Account.DoesNotExist: [if given email isn't found in database]
    """
    request.POST._mutable = True
    user_email = request.data.get('user')
    user_qs = Account.objects.get(email=user_email)
    print(type(user_qs))
    if not user_qs:
        raise Account.DoesNotExist('No such account exists')
    if user_qs:
        user_id = user_qs.id
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
    result = {}
    result['status'] = kwargs['status']
    result['message'] = kwargs['message']
    result['status'] = kwargs['status']
    result['message'] = kwargs['message']

    return result
