from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models

ROLE = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not email:
            raise ValueError('Заполнять поле email обязательно!!!!111')
        if not username:
            raise ValueError('Заполнять поле username обязательно!!!1!')
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, ):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_staff = True
        user.role = 'admin'
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя', max_length=50, blank=False, unique=True)
    email = models.EmailField('Email', blank=False, unique=True,
                              validators=[validators.validate_email])
    bio = models.TextField('О себе', blank=True)
    confirmation_code = models.CharField('Код подтверждения', max_length=30,
                                         blank=True, null=True)
    role = models.CharField('Права юзера', max_length=150, choices=ROLE, default='user')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    def change_help_text(self):
        self.is_active.help_text = 'мой текст'
        self.is_active.verbose_name = 'Активен'
        return self.is_active

    @property
    def is_user(self):
        return True if not self.is_staff else None

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
