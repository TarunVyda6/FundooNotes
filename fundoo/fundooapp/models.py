from django.db import models


class UserDetails(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    user_name = models.CharField(max_length=20)
    email_id = models.EmailField(max_length=50)
    password = models.CharField(max_length=15)
