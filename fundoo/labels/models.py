from __future__ import absolute_import
from django.db import models
from fundooapp.models import Account


class Label(models.Model):
    """
    this class is used to create an label for user
    """
    label_name = models.CharField(max_length=50)  # for label name
    created_time = models.DateTimeField(auto_now_add=True, null=True)  # created time of labels
    updated_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)  # user details
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        """
        this method is used to change status of is_deleted to true
        """
        self.is_deleted = True
        self.save()
