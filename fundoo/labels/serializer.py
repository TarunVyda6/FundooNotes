from rest_framework import serializers
from .models import Label


class LabelSerializer(serializers.ModelSerializer):
    # Serializer for Labels

    class Meta:
        model = Label
        fields = ('user', 'label_name')