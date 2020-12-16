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
        fields = ('user', 'title', 'description', 'is_archived',
                  'color', 'image', 'is_pinned',
                  'is_deleted', 'label', 'collaborate', 'archive_time', 'trash_time', 'reminder_date')
