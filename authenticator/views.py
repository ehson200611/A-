from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import AdminUser, NotificationAdmin, UserProfile
from .serializers import (
    RegisterSerializer, LoginSerializer, NotificationSerializer, 
    UserProfileSerializer, AdminUserListSerializer, AdminUserDetailSerializer,
    AdminUserUpdateRoleSerializer
)
from .permissions import IsSuperAdmin

User = get_user_model()


# --- REGISTER ---
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# --- LOGIN ---
class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phoneNumber']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(phoneNumber=phone_number)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=400)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=400)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=200)


# --- ADMIN USER MANAGEMENT ---
class AdminUserViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]    
    queryset = AdminUser.objects.all().order_by('-date_joined')

    def get_serializer_class(self):
        if self.action == 'list':
            return AdminUserListSerializer
        elif self.action == 'update_role':
            return AdminUserUpdateRoleSerializer
        return AdminUserDetailSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return AdminUser.objects.none()
        
        # Ҳамаи корбарон ҳамаи корбаронро мебинанд
        return AdminUser.objects.all().order_by('-date_joined')

    @action(detail=True, methods=['patch'], url_path='update-role')
    def update_role(self, request, pk=None):
        """Обновление роли пользователя (ҳоло барои ҳама дастрас аст)"""
        user = self.get_object()
        
        # Пешгирӣ аз тағири роли худ
        if user.id == request.user.id:
            return Response(
                {"error": "Cannot change your own role"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AdminUserUpdateRoleSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": f"User role updated to {serializer.validated_data['role']}",
            "user": AdminUserDetailSerializer(user).data
        })

    @action(detail=True, methods=['post'], url_path='activate')
    def activate_user(self, request, pk=None):
        """Активация пользователя (ҳоло барои ҳама дастрас аст)"""
        user = self.get_object()
        user.is_active = True
        user.save()

        return Response({
            "message": "User activated successfully",
            "user": AdminUserDetailSerializer(user).data
        })

    @action(detail=True, methods=['post'], url_path='deactivate')
    def deactivate_user(self, request, pk=None):
        """Деактивация пользователя (ҳоло барои ҳама дастрас аст)"""
        user = self.get_object()
        
        # Пешгирӣ аз деактиватсияи худ
        if user.id == request.user.id:
            return Response(
                {"error": "Cannot deactivate your own account"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_active = False
        user.save()

        return Response({
            "message": "User deactivated successfully",
            "user": AdminUserDetailSerializer(user).data
        })


# --- NOTIFICATIONS ---
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]  # ✅ Танҳо authentication лозим аст

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return NotificationAdmin.objects.none()
        if not self.request.user.is_authenticated:
            return NotificationAdmin.objects.none()
        return NotificationAdmin.objects.filter(user=self.request.user).order_by("-date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notif = self.get_object()
        notif.status = "read"
        notif.save()
        return Response({"message": "Notification marked as read"})


# --- USER PROFILE ---
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]  # ✅ Танҳо authentication лозим аст

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)