from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.serializers import SignUpSerializer, ConformationCodeSerializer, \
    UserSerializer
from users.models import User
from users.services import send_code_to_email, confirm_user

OK_STATUS = status.HTTP_200_OK
BAD_STATUS = status.HTTP_400_BAD_REQUEST


class UserCreate(APIView):
    """Вью для отображения регистрации пользователя и отправки сообщения на указанный mail
    кода подтверждения.
    """
    queryset = get_user_model()
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            serializer.save()
            send_code_to_email(username, email)
            return JsonResponse({'email': email, 'username': username}, status=OK_STATUS)


class TokenAPIView(APIView):
    """Вью для подтверждения полного доступа к сайту зарегистрированного пользователя."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = ConformationCodeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            confirm_user(serializer=serializer)
            return JsonResponse({'Статус': "Зарегистрирован"}, status=OK_STATUS)
        return JsonResponse(
                {'Статус': 'Неверный код подтверждения'}, status=BAD_STATUS)


class UserAPIView(ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
