from .models import NewUser
from rest_framework.serializers import ModelSerializer


class UserDetailsSerializer(ModelSerializer):
    class Meta:
        model = NewUser
        fields = '__all__'
