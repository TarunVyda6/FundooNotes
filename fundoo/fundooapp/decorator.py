from rest_framework import status
from django.http import HttpResponse
import json
from fundooapp.models import *
import jwt
from services.cache import Cache
from services.encrypt import Encrypt
import logging


def user_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        result = {'message': 'some other issue please try after some time', 'status': False}
        try:
            token = request.META['HTTP_AUTHORIZATION']
            decoded_token = Encrypt.decode(token)
            if Cache.get_cache("TOKEN_"+str(decoded_token['id'])+"_AUTH") is not None:
                request.user = Account.objects.get(id=decoded_token['id'])
                result['message'] = 'token verification successful'
                result['status'] = True
                logging.debug('{} status_code = {}'.format(result, status.HTTP_200_OK))
                return view_func(request, *args, **kwargs)

            result['message'] = "logged in user's token is not provided"
            logging.debug('{} status_code = {}'.format(result, status.HTTP_400_BAD_REQUEST))
            return HttpResponse(json.dumps(result), status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError as e:
            result['message'] = 'Activation Expired'
            logging.exception('{} exception = {}, status_code = {}'.format(result, str(e), status.HTTP_400_BAD_REQUEST))
            return HttpResponse(json.dumps(result), status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            result['message'] = 'Invalid Token'
            logging.exception('{}, exception = {}, status_code = {}'.format(result, str(e), status.HTTP_400_BAD_REQUEST))
            return HttpResponse(json.dumps(result), status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result['message'] = 'some other issue please try after some time'
            logging.exception('{}, exception = {}, status_code = {}'.format(result, str(e),  status.HTTP_400_BAD_REQUEST))
            return HttpResponse(json.dumps(result), status.HTTP_400_BAD_REQUEST)

    return wrapper