# authenticator/simple_views.py
from rest_framework import generics, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import AdminUser, NotificationAdmin, UserProfile
from .serializers import (
    RegisterSerializer, LoginSerializer, NotificationSerializer, 
    UserProfileSerializer, UserProfilePDFSerializer, AdminUserListSerializer, AdminUserDetailSerializer,
    AdminUserUpdateRoleSerializer, TestAdminSerializer, AdminRoleSerializer
)
from .permissions import IsSuperAdmin, IsAdminOrSuperAdmin, IsOwnerOrAdmin
from rest_framework.views import APIView
from tests.models import TestResult

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

# --- ADMIN USER MANAGEMENT (упрощенная версия) ---
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

# --- USER PROFILE (упрощенная версия) ---
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

# --- CURRENT USER PROFILE ---
class CurrentUserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        try:
            return UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(
                user=self.request.user,
                phone=self.request.user.phoneNumber,
                status='active',
                is_pdf=False
            )
            return profile

# --- NOTIFICATIONS ---
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

# --- SUPER ADMIN LIST ---
class SuperAdminListView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        superadmins = AdminUser.objects.filter(role="superadmin")
        serializer = AdminUserListSerializer(superadmins, many=True)

        return Response({
            "count": superadmins.count(),
            "superadmins": serializer.data
        })

# --- TEST ADMIN ---
class TestAdminViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TestAdminSerializer
    queryset = TestResult.objects.all().order_by("-dateCompleted")
    
    def get_permissions(self):
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

# --- CURRENT USER NOTIFICATIONS ---
class CurrentUserNotificationsView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NotificationAdmin.objects.filter(user=self.request.user).order_by("-date")