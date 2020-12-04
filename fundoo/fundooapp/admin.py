from django.contrib import admin
from .models import UserDetails


# Register your models here.

class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'user_name', 'email_id', 'password']


admin.site.register(UserDetails, UserDetailsAdmin)
