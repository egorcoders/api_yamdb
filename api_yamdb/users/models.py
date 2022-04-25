from django.contrib.auth.models import AbstractUser
from django.db import models

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
USER_ROLES = [
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin'),
]


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя', max_length=50, blank=False, unique=True)
    email = models.EmailField('Email', blank=False, unique=True)
    bio = models.TextField('О себе', blank=True)
    confirmation_code = models.CharField('Код подтверждения', max_length=30,)
    role = models.CharField(
        'Роль', max_length=150, blank=False,
        choices=USER_ROLES, default='user',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username
