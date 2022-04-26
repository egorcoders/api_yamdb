from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'is_superuser',
        'moderator',
        'admin',
        'date_joined'
    )
    search_fields = ('username',)
    empty_value_display = '-empty-'
    ordering = ['-date_joined']
    fieldsets = (
        ('Персональные данные', {'fields': ('username', 'email', 'date_joined')}),
        ('Административные права', {'fields': ('is_active', 'moderator', 'admin', 'is_superuser',)}),
        ('Прочее', {'fields': ('bio', 'password')}),
    )