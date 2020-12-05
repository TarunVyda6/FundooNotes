from __future__ import absolute_import
from rest_framework.viewsets import ModelViewSet
from .models import NewUser
from fundooapp.serializers import UserDetailsSerializer


class UserDetailsCrud(ModelViewSet):
    queryset = NewUser.objects.all()
    serializer_class = UserDetailsSerializer
