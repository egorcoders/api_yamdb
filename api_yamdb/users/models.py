from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager
from django.core import validators
from django.db import models

ROLES = (('user', 'User'),
         ('moderator', 'Moder'),
         ('admin', 'Admin'),)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not email:
            raise ValueError('Заполнять поле email обязательно')
        if not username:
            raise ValueError('Заполнять поле username обязательно')
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password,):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя', max_length=50, blank=False, unique=True)
    email = models.EmailField('Email', blank=False, unique=True, validators=[validators.validate_email])
    bio = models.TextField('О себе', blank=True)
    confirmation_code = models.CharField('Код подтверждения', max_length=30, blank=True, null=True)
    role = models.CharField(
        max_length=20, choices=ROLES, default='user', blank=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
