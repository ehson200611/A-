# authenticator/simple_views.py (исправленная версия)
from rest_framework import generics, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import AdminUser, NotificationAdmin, PasswordResetCode, UserProfile
from .serializers import (
    ForgotPasswordSerializer, RegisterSerializer, LoginSerializer, NotificationSerializer, ResetPasswordSerializer, 
    UserProfileSerializer, UserProfilePDFSerializer, AdminUserListSerializer, AdminUserDetailSerializer,
    AdminUserUpdateRoleSerializer, TestAdminSerializer, AdminRoleSerializer, VerifyCodeSerializer
)
from .permissions import IsSuperAdmin, IsAdminOrSuperAdmin, IsOwnerOrAdmin
from rest_framework.views import APIView
from tests.models import TestResult
from .token import get_tokens_for_user  # Ҷойи функсияи тавлиди токен
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema


User = get_user_model()

# --- РЕГИСТРАЦИЯ ---
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# --- АВТОРИЗАЦИЯ ---
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .serializers import LoginSerializer
from .token import get_tokens_for_user  # Ҷойи функсияи тавлиди токен

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        # 1. Сериализатсия кардани маълумот
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phoneNumber']
        password = serializer.validated_data['password']

        # 2. Верификация кардани корбар
        try:
            user = authenticate(phoneNumber=phone_number, password=password)
        except:
            return Response({"error": "Invalid credentials"}, status=400)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=400)

        # 3. Агар корбар дуруст бошад, токенҳо месозем
        if user.is_active:
            tokens = get_tokens_for_user(user)

            return Response({
                "refresh": tokens["refresh"],  # Refresh token
                "access": tokens["access"],  # Access token
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "phoneNumber": user.phoneNumber,
                    "role": user.role,
                    "is_active": user.is_active
                }
            }, status=200)

        return Response({"error": "Account is deactivated"}, status=400)



# --- ОТДЕЛЬНЫЕ ФУНКЦИИ ДЛЯ ПОЛУЧЕНИЯ ПОЛЬЗОВАТЕЛЕЙ ---

def get_superadmins(request):
    """Отдельная функция для получения суперадминов"""
    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required"}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    if request.user.role != 'superadmin' and not request.user.is_superuser:
        return Response(
            {"error": "Only superadmins can view superadmins list"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    superadmins = AdminUser.objects.filter(role="superadmin").order_by('-date_joined')
    serializer = AdminUserListSerializer(superadmins, many=True)
    
    return Response({
        "count": superadmins.count(),
        "superadmins": serializer.data
    })

def get_admins(request):
    """Отдельная функция для получения админов"""
    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required"}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    if request.user.role not in ['superadmin', 'admin'] and not request.user.is_superuser:
        return Response(
            {"error": "Only admins can view admins list"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Суперадмины видят всех админов
    if request.user.role == 'superadmin' or request.user.is_superuser:
        admins = AdminUser.objects.filter(role="admin").order_by('-date_joined')
    # Обычные админы видят только других админов (но не себя)
    else:
        admins = AdminUser.objects.filter(
            role="admin"
        ).exclude(id=request.user.id).order_by('-date_joined')
    
    serializer = AdminUserListSerializer(admins, many=True)
    
    return Response({
        "count": admins.count(),
        "admins": serializer.data
    })

def get_regular_users(request):
    """Отдельная функция для получения обычных пользователей"""
    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required"}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    if request.user.role not in ['superadmin', 'admin'] and not request.user.is_superuser:
        return Response(
            {"error": "Only admins can view regular users list"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    regular_users = AdminUser.objects.filter(role="user").order_by('-date_joined')
    serializer = AdminUserListSerializer(regular_users, many=True)
    
    return Response({
        "count": regular_users.count(),
        "regular_users": serializer.data
    })

# --- VIEWSET ДЛЯ УПРАВЛЕНИЯ АДМИНАМИ ---
class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = AdminUser.objects.all().order_by('-date_joined')
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsSuperAdmin]
        elif self.action == 'list':
            permission_classes = [IsAdminOrSuperAdmin]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrAdmin | IsSuperAdmin]
        elif self.action in ['update_role', 'activate_user', 'deactivate_user']:
            permission_classes = [IsSuperAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return AdminUserListSerializer
        elif self.action == 'update_role':
            return AdminUserUpdateRoleSerializer
        return AdminUserDetailSerializer

    def get_queryset(self):
        user = self.request.user
        
        if not user.is_authenticated:
            return AdminUser.objects.none()
        
        if user.role == 'superadmin' or user.is_superuser:
            return AdminUser.objects.all().order_by('-date_joined')
        elif user.role == 'admin':
            return AdminUser.objects.exclude(role='superadmin').order_by('-date_joined')
        else:
            return AdminUser.objects.filter(id=user.id)

    @action(detail=True, methods=['patch'], url_path='update-role')
    def update_role(self, request, pk=None):
        user = self.get_object()
        
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
        user = self.get_object()
        user.is_active = True
        user.save()

        return Response({
            "message": "User activated successfully",
            "user": AdminUserDetailSerializer(user).data
        })

    @action(detail=True, methods=['post'], url_path='deactivate')
    def deactivate_user(self, request, pk=None):
        user = self.get_object()
        
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

# --- VIEW ДЛЯ ПРОФИЛЕЙ ПОЛЬЗОВАТЕЛЕЙ ---
class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAdminOrSuperAdmin]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsOwnerOrAdmin]
        elif self.action == 'create':
            permission_classes = [IsSuperAdmin]
        else:
            permission_classes = [IsSuperAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        
        if not user.is_authenticated:
            return UserProfile.objects.none()
        
        if user.role in ['superadmin', 'admin'] or user.is_superuser:
            return UserProfile.objects.all()
        
        return UserProfile.objects.filter(user=user)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        profile = self.get_object()
        new_status = request.data.get("status")

        if new_status not in ["active", "inactive", "pending"]:
            return Response({"error": "Invalid status"}, status=400)

        profile.status = new_status
        profile.save()

        return Response({
            "message": "Status updated",
            "profile": UserProfileSerializer(profile).data
        })

    @action(detail=True, methods=['patch'], url_path='update-pdf-status')
    def update_pdf_status(self, request, pk=None):
        profile = self.get_object()
        
        serializer = UserProfilePDFSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            profile_serializer = UserProfileSerializer(profile)
            return Response({
                "message": "PDF status updated successfully",
                "profile": profile_serializer.data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='pdf-profiles')
    def pdf_profiles(self, request):
        queryset = self.get_queryset().filter(is_pdf=True)
        serializer = UserProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='non-pdf-profiles')
    def non_pdf_profiles(self, request):
        queryset = self.get_queryset().filter(is_pdf=False)
        serializer = UserProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='toggle-pdf')
    def toggle_pdf(self, request, pk=None):
        profile = self.get_object()
        
        profile.is_pdf = not profile.is_pdf
        profile.pdf_updated_at = timezone.now()
        profile.save()
        
        return Response({
            "message": f"PDF status toggled to {profile.is_pdf}",
            "profile": UserProfileSerializer(profile).data
        })

# --- ТЕКУЩИЙ ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ ---
class CurrentUserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        try:
            return UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            return UserProfile.objects.create(
                user=self.request.user,
                phone=self.request.user.phoneNumber,
                status='active'
            )




# --- УВЕДОМЛЕНИЯ ---
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = NotificationAdmin.objects.all()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [IsAdminOrSuperAdmin]
        else:
            permission_classes = [IsAdminOrSuperAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        
        if not user.is_authenticated:
            return NotificationAdmin.objects.none()
        
        if user.role in ['superadmin', 'admin'] or user.is_superuser:
            return NotificationAdmin.objects.all().order_by("-date")
        
        return NotificationAdmin.objects.filter(user=user).order_by("-date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'], url_path="mark-read")
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.status = "read"
        notification.save()
        return Response({"message": "Notification marked as read"})

    @action(detail=True, methods=['post'], url_path="mark-unread")
    def mark_unread(self, request, pk=None):
        notification = self.get_object()
        notification.status = "unread"
        notification.save()
        return Response({"message": "Notification marked as unread"})

# --- API VIEW ДЛЯ ОТДЕЛЬНЫХ ФУНКЦИЙ ---

class SuperAdminListAPIView(APIView):
    """API View для получения списка суперадминов"""
    permission_classes = [IsSuperAdmin]
    
    def get(self, request):
        return get_superadmins(request)

class AdminListAPIView(APIView):
    """API View для получения списка админов"""
    permission_classes = [IsAdminOrSuperAdmin]
    
    def get(self, request):
        return get_admins(request)

class RegularUsersListAPIView(APIView):
    """API View для получения списка обычных пользователей"""
    permission_classes = [IsAdminOrSuperAdmin]
    
    def get(self, request):
        return get_regular_users(request)

# --- ТЕСТЫ АДМИНИСТРАТОРА ---
class TestAdminViewSet(viewsets.ModelViewSet):
    serializer_class = TestAdminSerializer
    queryset = TestResult.objects.all().order_by("-dateCompleted")
    
    def get_permissions(self):
        if self.action in ['list', 'create']:
            permission_classes = [IsAdminOrSuperAdmin]
        else:
            permission_classes = [IsAdminOrSuperAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        
        if not user.is_authenticated:
            return TestResult.objects.none()
        
        if user.role == 'superadmin' or user.is_superuser:
            return TestResult.objects.all().order_by("-dateCompleted")
        elif user.role == 'admin':
            return TestResult.objects.all().order_by("-dateCompleted")
        
        return TestResult.objects.filter(profile__user=user).order_by("-dateCompleted")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = TestAdminSerializer(queryset, many=True).data
        return Response({"testAdmin": data})

    def create(self, request, *args, **kwargs):
        serializer = TestAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"created": serializer.data}, status=201)

# --- ТЕКУЩИЕ УВЕДОМЛЕНИЯ ПОЛЬЗОВАТЕЛЯ ---  
class CurrentUserNotificationsView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NotificationAdmin.objects.filter(user=self.request.user).order_by("-date")
    



from drf_spectacular.utils import extend_schema

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=ForgotPasswordSerializer,
        responses={200: OpenApiTypes.OBJECT}
    )
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phoneNumber']

        try:
            user = AdminUser.objects.get(phoneNumber=phone)
        except AdminUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        import random
        code = str(random.randint(100000, 999999))

        PasswordResetCode.objects.create(phoneNumber=phone, code=code)

        print("RESET CODE:", code)

        return Response({"message": "Reset code sent"})



class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=ResetPasswordSerializer,
        responses={200: OpenApiTypes.OBJECT}
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phoneNumber']
        code = serializer.validated_data['code']
        password = serializer.validated_data['password']

        try:
            reset = PasswordResetCode.objects.filter(phoneNumber=phone).latest('created_at')
        except PasswordResetCode.DoesNotExist:
            return Response({"error": "Invalid reset request"}, status=404)

        if reset.code != code:
            return Response({"error": "Invalid code"}, status=400)

        if reset.is_expired():
            return Response({"error": "Code expired"}, status=400)

        try:
            user = AdminUser.objects.get(phoneNumber=phone)
        except AdminUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        user.set_password(password)
        user.save()

        return Response({"message": "Password reset successfully"})


class VerifyResetCodeView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=VerifyCodeSerializer,
        responses={200: OpenApiTypes.OBJECT}
    )
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phoneNumber']
        code = serializer.validated_data['code']

        try:
            reset = PasswordResetCode.objects.filter(phoneNumber=phone).latest('created_at')
        except PasswordResetCode.DoesNotExist:
            return Response({"error": "Code not found"}, status=404)

        if reset.code != code:
            return Response({"error": "Invalid code"}, status=400)

        if reset.is_expired():
            return Response({"error": "Code expired"}, status=400)

        return Response({"message": "Code verified"})

