from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note

User = get_user_model()


# Note serializer for storing user created notes to database

class NoteSerializer(serializers.ModelSerializer):
    # Serializer for Notes

    class Meta:
        model = Note
        fields = '__all__'