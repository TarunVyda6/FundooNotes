from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin


class UserDetailsAdmin(UserAdmin):
    """
    this class is used to setup the look of the admin panel
    """
    model = Account
    ordering = ('email', 'first_name', 'last_name', 'user_name')
    list_display = ['user_name', 'email']
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name', 'last_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_verified')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'email', 'first_name', 'last_name', 'user_name', 'password', 'is_active', 'is_staff', 'is_verified')}
         ),
    )


admin.site.register(Account, UserDetailsAdmin)