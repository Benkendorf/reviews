from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        ('Основные данные пользователя', {
            'fields': ('username', 'email'),
        }),
        ('Персональная информация пользователя', {
            'fields': ('first_name', 'last_name', 'bio'),
        }),
        ('Роли пользователя', {
            'fields': ("is_superuser", 'role'),
        }),
    )

    list_display = ('username', 'email', 'role', 'first_name', 'last_name')
    list_editable = ('email', 'first_name', 'last_name', 'role')
    search_fields = ('first_name', 'last_name', 'email', 'username')
    list_filter = ('role',)
