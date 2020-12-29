from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note

User = get_user_model()


class NoteSerializer(serializers.ModelSerializer):
    """
    this class is used for serialization and deserialization of notes
    """

    class Meta:
        model = Note
        fields = '__all__'
