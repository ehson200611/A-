# authenticator/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, 
    LoginView,
    AdminUserViewSet, 
    NotificationViewSet,
    UserProfileViewSet, 
    SuperAdminListView,
    TestAdminViewSet, 
    CurrentUserProfileView,
    CurrentUserNotificationsView
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
    
    # Суперадмины
    path('superadmins/', SuperAdminListView.as_view(), name='superadmin-list'),
    
    # API endpoints
    path('', include(router.urls)),
]