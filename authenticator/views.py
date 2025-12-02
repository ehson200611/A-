# authenticator/views.py
from rest_framework import generics, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from .models import AdminUser, NotificationAdmin, UserProfile
from .serializers import (
    RegisterSerializer, LoginSerializer, NotificationSerializer, 
    UserProfileSerializer, AdminUserListSerializer, AdminUserDetailSerializer,
    AdminUserUpdateRoleSerializer, TestAdminSerializer
)
from rest_framework.views import APIView
from tests.models import TestResult
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

User = get_user_model()

# --- PERMISSION CLASSES ---
class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and 
                   (request.user.is_superuser or request.user.role == 'superadmin'))


class IsAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in ['admin', 'superadmin'] or request.user.is_superuser


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role in ['admin', 'superadmin'] or request.user.is_superuser:
            return True
        return obj.user == request.user


# --- REGISTER и LOGIN остаются публичными ---
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # Публичный


@extend_schema(
    tags=['Authentication'],
    summary='Login to get JWT token',
    description='Authenticate user and return JWT tokens',
    request=LoginSerializer,
)
class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]  # Публичный
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

        if not user.is_active:
            return Response({"error": "Account is deactivated"}, status=400)

        refresh = RefreshToken.for_user(user)
        
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "name": user.name,
                "phoneNumber": user.phoneNumber,
                "role": user.role,
                "is_active": user.is_active
            }
        }, status=200)


# --- ADMIN USER MANAGEMENT (полностью защищенный) ---
@extend_schema_view(
    list=extend_schema(
        summary='List all admin users',
        description='Get list of all admin users (admin only)',
        parameters=[
            OpenApiParameter(name='role', description='Filter by role', required=False, type=str),
        ]
    ),
    retrieve=extend_schema(
        summary='Retrieve admin user',
        description='Get detailed information about specific admin user (admin only)',
    ),
    create=extend_schema(
        summary='Create admin user',
        description='Create new admin user (superadmin only)',
    ),
    update=extend_schema(
        summary='Update admin user',
        description='Update admin user information (admin only)',
    ),
    partial_update=extend_schema(
        summary='Partial update admin user',
        description='Partially update admin user information (admin only)',
    ),
    destroy=extend_schema(
        summary='Delete admin user',
        description='Delete admin user (superadmin only)',
    ),
)
class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = AdminUser.objects.all().order_by('-date_joined')
    
    def get_permissions(self):
        # Все действия требуют авторизации
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

    @extend_schema(
        summary='Update user role',
        description='Update role of a user (superadmin only)',
        request=AdminUserUpdateRoleSerializer,
    )
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

    @extend_schema(
        summary='Activate user',
        description='Activate a user account (superadmin only)',
    )
    @action(detail=True, methods=['post'], url_path='activate')
    def activate_user(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()

        return Response({
            "message": "User activated successfully",
            "user": AdminUserDetailSerializer(user).data
        })

    @extend_schema(
        summary='Deactivate user',
        description='Deactivate a user account (superadmin only)',
    )
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


# --- NOTIFICATIONS (защищенный) ---
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    
    def get_permissions(self):
        # Все действия требуют авторизации
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


# --- USER PROFILE (защищенный) ---
class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    
    def get_permissions(self):
        # Все действия требуют авторизации
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


# --- SUPER ADMIN LIST (защищенный) ---
class SuperAdminListView(APIView):
    permission_classes = [IsSuperAdmin]  # Только суперадмины

    def get(self, request):
        superadmins = AdminUser.objects.filter(role="superadmin")
        serializer = AdminUserListSerializer(superadmins, many=True)

        return Response({
            "count": superadmins.count(),
            "superadmins": serializer.data
        })


# --- TEST ADMIN (защищенный) ---
class TestAdminViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TestAdminSerializer
    
    def get_permissions(self):
        # Только для админов
        if self.action == 'list':
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


# --- CURRENT USER PROFILE (защищенный) ---
class CurrentUserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Только авторизованные

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(
                user=request.user,
                phone=request.user.phoneNumber,
                status='active'
            )
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data, status=201)

    def put(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(
                user=request.user,
                phone=request.user.phoneNumber,
                status='active'
            )
        
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


# --- CURRENT USER NOTIFICATIONS (защищенный) ---
class CurrentUserNotificationsView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]  # Только авторизованные

    def get_queryset(self):
        return NotificationAdmin.objects.filter(user=self.request.user).order_by("-date")