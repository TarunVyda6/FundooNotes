from __future__ import absolute_import

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import UserDetails
from fundooapp.serializers import UserDetailsSerializer



class UserDetailsCrud(ModelViewSet):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer
