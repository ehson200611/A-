from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import AdminUser, NotificationAdmin, AdminForSuperAdmin, TestAdmin
from .serializers import (
    AdminUserSerializer, NotificationAdminSerializer,
    AdminForSuperAdminSerializer, TestAdminSerializer
)

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = AdminUser.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [AllowAny]

class NotificationAdminViewSet(viewsets.ModelViewSet):
    queryset = NotificationAdmin.objects.all()
    serializer_class = NotificationAdminSerializer
    permission_classes = [AllowAny]

class AdminForSuperAdminViewSet(viewsets.ModelViewSet):
    queryset = AdminForSuperAdmin.objects.all()
    serializer_class = AdminForSuperAdminSerializer
    permission_classes = [AllowAny]

class TestAdminViewSet(viewsets.ModelViewSet):
    queryset = TestAdmin.objects.all()
    serializer_class = TestAdminSerializer
    permission_classes = [AllowAny]
