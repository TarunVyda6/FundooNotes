from __future__ import absolute_import
from django.db import models
from fundooapp.models import Account


# Label model
class Label(models.Model):
    label_name = models.CharField(max_length=50)  # for label name
    created_time = models.DateTimeField(auto_now_add=True, null=True)  # created time of labels
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)  # user details

    def __str__(self):
        return self.label_name
