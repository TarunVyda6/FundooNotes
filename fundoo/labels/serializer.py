from rest_framework import serializers
from .models import Label


class LabelSerializer(serializers.ModelSerializer):
    """
    this class is used to serialization and deserialization of labels
    """

    class Meta:
        model = Label
        fields = ('user', 'label_name')
