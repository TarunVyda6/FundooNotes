from rest_framework import status
from django.http import HttpResponse
import json
from fundooapp.models import Account
import jwt


def user_login_required(view_func):

    def wrapper(request, *args, **kwargs):

        try:
            token = request.META['HTTP_AUTHORIZATION']
            decoded_token = jwt.decode(token, "secret", algorithms=["HS256"])
            print(token)
            email = decoded_token['email']
            user = Account.objects.get(email=email)
            try:
                if user and user.is_active:
                    request.user = user
                    return view_func(request, *args, **kwargs)
            except Account.DoesNotExist:
                response = {'success': False, 'message': 'User must be logged in'}
                return HttpResponse(json.dumps(response), status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            if request.session:
                user = request.user
                if user.is_authenticated:
                    return view_func(request, *args, **kwargs)
                else:
                    smd = {'success': False, 'message': 'Please provide valid credentials..!!'}
                    return HttpResponse(json.dumps(smd), status=status.HTTP_400_BAD_REQUEST)
            else:
                smd = {'success': False, 'message': 'User must be logged in'}
                return HttpResponse(json.dumps(smd), status=status.HTTP_400_BAD_REQUEST)

    return wrapper
