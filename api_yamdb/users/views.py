from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import (
    SignUpSerializer, ConformationCodeSerializer, UserSerializer)
from .models import User
from .services import send_code_to_email, confirm_user

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
            token = confirm_user(serializer=serializer)
            return JsonResponse({'token': token}, status=OK_STATUS)
        return JsonResponse(
                {'Статус': 'Неверный код подтверждения'}, status=BAD_STATUS)


class UserAPIView(ModelViewSet):
    """Вью для отображения всех пользователей сайта."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=('GET', 'PATCH',), detail=False, url_path='me', permission_classes=(IsAuthenticated,)
    )
    def get_me(self, request):
        """Формирует эндпоинт авторизованного пользователя, сделавшего запрос."""
        try:
            user = User.objects.get(pk=request.user.pk)
        except ObjectDoesNotExist as e:
            raise e
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return JsonResponse({'data': serializer.data}, status=OK_STATUS)
