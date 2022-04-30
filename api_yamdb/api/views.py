from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404

from reviews.models import Title, Review, Category, Genre
from .serializers import (
    ReviewSerializer, CommentSerializer,
    CategorySerializer, GenreSerializer,
    TitleViewSerializer, TitleWriteSerializer,
)
from .permissions import IsAuthorOrModeratorOrAdminOrReadOnly
from .pagination import ReviewsPagination, CommentsPagination


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthorOrModeratorOrAdminOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    ]
    pagination_class = ReviewsPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthorOrModeratorOrAdminOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    ]
    pagination_class = CommentsPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(
            author=self.request.user,
            review=review
        )


class TitleViewSet(viewsets.ModelViewSet):
    '''Вьюсет произведений.'''
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleWriteSerializer
        return TitleViewSerializer


class GenreViewSet(viewsets.ModelViewSet):
    '''Вьюсет жанров.'''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    '''Вьюсет категорий.'''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
