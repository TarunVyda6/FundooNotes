from .models import UserDetails
from rest_framework.serializers import ModelSerializer


class UserDetailsSerializer(ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'
