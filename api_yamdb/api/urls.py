from rest_framework import routers
from django.urls import include, path

from api.views import (
    ReviewViewSet, CommentViewSet, CategoryViewSet,
    GenreViewSet, TitleViewSet
)
from users.views import UserAPIView


router = routers.DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router.register(r'users', UserAPIView, basename='users')
router.register(r'^categories', CategoryViewSet, basename='categories'),
router.register(r'^genres', GenreViewSet, basename='genres'),
router.register(r'^titles', TitleViewSet, basename='titles'),

urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path('v1/', include(router.urls)),
]
