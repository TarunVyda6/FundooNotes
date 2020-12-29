from __future__ import absolute_import

from colorfield.fields import ColorField
from django.db import models
from fundooapp.models import Account
from labels.models import Label


class Note(models.Model):
    """
    this class is used to create model for user
    """
    title = models.CharField(max_length=150, default=None)  # for add title
    description = models.TextField()  # for add descriptions
    created_time = models.DateTimeField(auto_now_add=True, null=True)  # for created time which is auto
    updated_time = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)  # for archive notes
    is_deleted = models.BooleanField(default=False)  # for delete notes
    color = ColorField(default='#00F0FF')  # for set color
    image = models.ImageField(upload_to='note_images/', default=None, null=True)  # for set image to notes
    trash = models.BooleanField(default=False)  # for trash notes
    is_pinned = models.BooleanField(default=False)  # for set pin unpin notes
    label = models.ManyToManyField(Label)  # for label names
    collaborate = models.ManyToManyField(Account, blank=True, related_name='collaborated_user')  # for
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='owner', null=True, blank=True)  # for

    def __str__(self):
        return self.title + " " + self.description

    def soft_delete(self):
        """
        this class is used to change the status of is_deleted to true
        """
        self.is_deleted = True
        self.save()
