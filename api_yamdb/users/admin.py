from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'pk',
        'username',
        'is_superuser',
        'role',)
    search_fields = ('username',)
    list_filter = ('role',)
    empty_value_display = '-empty-'
