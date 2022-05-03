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
    ReviewViewSet, basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'
)
router.register(r'users', UserAPIView, basename='users')
router.register(r'^categories', CategoryViewSet, basename='category'),
router.register(r'^genres', GenreViewSet, basename='genre'),
router.register(r'^titles', TitleViewSet, basename='title'),

urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path('v1/', include(router.urls)),
]
