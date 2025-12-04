# authenticator/urls.py (обновленная версия)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .simple_views import (
    RegisterView, 
    LoginView,
    AdminUserViewSet, 
    NotificationViewSet,
    UserProfileViewSet, 
    SuperAdminListAPIView,
    AdminListAPIView,
    RegularUsersListAPIView,
    TestAdminViewSet, 
    CurrentUserProfileView,
    CurrentUserNotificationsView,
    get_superadmins,  # Импортируем отдельные функции
    get_admins,
    get_regular_users
) 

router = DefaultRouter()
router.register(r'users', AdminUserViewSet, basename='adminuser')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'profiles', UserProfileViewSet, basename='userprofile')
router.register(r'tests-admin', TestAdminViewSet, basename='testadmin')

urlpatterns = [
    # Аутентификация
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    # Текущий пользователь
    path('me/profile/', CurrentUserProfileView.as_view(), name='current-user-profile'),
    path('me/notifications/', CurrentUserNotificationsView.as_view(), name='current-user-notifications'),
    
    # Отдельные функции для получения пользователей (как API View)
    path('superadmins/', SuperAdminListAPIView.as_view(), name='superadmin-list'),
    path('admins/', AdminListAPIView.as_view(), name='admin-list'),
    path('regular-users/', RegularUsersListAPIView.as_view(), name='regular-users-list'),
    
    # API endpoints
    path('', include(router.urls)),
]