from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdminUserViewSet, NotificationAdminViewSet,
    AdminForSuperAdminViewSet, TestAdminViewSet
)

router = DefaultRouter()
router.register(r'users', AdminUserViewSet, basename='users')
router.register(r'notifications', NotificationAdminViewSet, basename='notifications')
router.register(r'superadmins', AdminForSuperAdminViewSet, basename='superadmins')
router.register(r'tests', TestAdminViewSet, basename='tests')

urlpatterns = [
    path('', include(router.urls)),
]
