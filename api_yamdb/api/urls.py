from django.urls import include, path

from rest_framework.routers import DefaultRouter

from users.views import UserAPIView

router = DefaultRouter()

router.register(r'users', UserAPIView, basename='users')

urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path('v1/', include(router.urls)),
]
