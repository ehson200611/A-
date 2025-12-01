from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdminUserViewSet,
    NotificationViewSet,
    UserProfileViewSet
)

router = DefaultRouter()
router.register('admin-users', AdminUserViewSet, basename='admin-users')
router.register('notifications', NotificationViewSet, basename='notifications')
router.register('profiles', UserProfileViewSet, basename='profiles')

urlpatterns = [
    path('', include(router.urls)),
]
