import random
import string
from smtplib import SMTPException
from typing import Any

from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import AccessToken

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
    user.save()
    return confirmation_code


def send_code_to_email(username: str, email: str) -> None:
    """Отправляет сообщение с кодом по переданному адресу."""
    confirmation_code = get_confirmation_code(username)
    try:
        email = EmailMessage(
            body=f'{username} для завершения регистрации ваш код {confirmation_code}',
            from_email=123,
            to=[f'{email}'],
        )
        email.send()
    except SMTPException as e:
        raise e


def confirm_user(serializer: Any) -> None:
    """Подтверждает регистрацию пользователя."""
    username = serializer.validated_data['username']
    user = User.objects.get(username=username)
    code = serializer.data['confirmation_code']
    if user.confirmation_code == code:
        create_token(user)


def create_token(user):
    """Создаем и присваиваем токен пользователю."""
    token = default_token_generator.make_token(user)
    if default_token_generator.check_token(user, token):
        try:
            AccessToken.for_user(user)
            user.is_active = True
            user.save()
            print(token)
            return token
        except Exception as e:
            raise e