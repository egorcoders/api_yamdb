import random
import string
from smtplib import SMTPException
from typing import Any, Dict

from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from users.models import User


def generate_code():
    """Генерирует случайны код из букв, цифр. Через цикл получаем строку, с кодом."""
    alphabet = string.digits + string.ascii_uppercase + string.ascii_letters
    code_to = str()
    for i in random.sample(alphabet, 6):
        code_to += i
    return code_to


def get_confirmation_code(username: str) -> str:
    """Получает токен определенного юзера и сохраняет его в confirmation_code"""
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist as e:
        raise e
    confirmation_code = generate_code()
    user.confirmation_code = confirmation_code
    user.is_active = False
    user.save()
    return confirmation_code


def send_code_to_email(username: str, email: str) -> None:
    """Отправляет сообщение с кодом по переданному адресу."""
    confirmation_code = get_confirmation_code(username)
    try:
        email = EmailMessage(
            body=f'{username} для завершения регистрации ваш код {confirmation_code}',
            from_email=EMAIL_HOST_USER,
            to=[f'{email}'],
        )
        email.send()
    except SMTPException as e:
        raise e


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def confirm_user(serializer: Any) -> Dict[str, str]:
    """Подтверждает регистрацию пользователя."""
    username = serializer.validated_data['username']
    user = User.objects.get(username=username)
    code = serializer.data['confirmation_code']
    if user.confirmation_code == code and user.username == username:
        token = get_tokens_for_user(user)
        user.is_active = True
        user.save()
        return token
