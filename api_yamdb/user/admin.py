from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id', 'username', 'email', 'role', 'first_name', 'last_name'
    )
    list_editable = ('role',)
    search_fields = ('first_name',)
    list_filter = ('username', 'role')
