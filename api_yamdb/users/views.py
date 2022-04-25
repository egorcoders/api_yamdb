from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny

from api.serializers import SignUpSerializer
from users.models import User


class UserCreate(generics.CreateAPIView):
    queryset = get_user_model()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny, )
