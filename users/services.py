import uuid
from smtplib import SMTPException
from typing import Dict

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


def get_confirmation_code(username: str) -> str:
    '''Получает токен определенного юзера
     и сохраняет его в confirmation_code.
     '''
    try:
        # при get_or_create() падают тесты
        user = User.objects.get(username=username)
    except ObjectDoesNotExist as e:
        raise e
    confirmation_code = str(uuid.uuid4())
    user.confirmation_code = confirmation_code
    user.is_active = False
    user.save()
    return confirmation_code


def send_code_to_email(username: str, email: str) -> None:
    '''Отправляет сообщение с кодом по переданному адресу.'''
    confirmation_code = get_confirmation_code(username)
    try:
        send_mail(
            'Confirmation code',
            f'{username} ваш код {confirmation_code}',
            settings.EMAIL_HOST_USER,
            [f'{email}'],
            fail_silently=False
        )
    except SMTPException as e:
        raise e


def get_tokens_for_user(user: str) -> Dict[str, str]:
    '''Создает токен пользователю.'''
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
