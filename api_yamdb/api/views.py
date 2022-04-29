from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from reviews.models import Category, Genre, Title

from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    '''Вьюсет произведений.'''
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    serializer_class = TitleSerializer


class GenreViewSet(viewsets.ModelViewSet):
    '''Вьюсет жанров.'''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    '''Вьюсет категорий.'''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer