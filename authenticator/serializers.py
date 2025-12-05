from rest_framework import serializers
from .models import AdminUser, NotificationAdmin, UserProfile
from tests.models import TestResult
from tests.serializers import TestResultSerializer
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes


class RegisterSerializer(serializers.ModelSerializer):
    passwordConfirm = serializers.CharField(write_only=True)

    class Meta:
        model = AdminUser
        fields = ['name', 'phoneNumber', 'password', 'passwordConfirm']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['passwordConfirm']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop("passwordConfirm")
        password = validated_data.pop("password")
        user = AdminUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField()
    password = serializers.CharField(write_only=True)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationAdmin
        fields = "__all__"
        read_only_fields = ["user", "status", "date"]


class UserProfileSerializer(serializers.ModelSerializer):
    # Тестҳои истифодабаранда
    tests = serializers.SerializerMethodField()

    # Барои баргардонидани номи юзер
    user_name = serializers.CharField(source='user.name', read_only=True)

    # role аз property меояд → source лозим нест!
    role = serializers.CharField(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user',
            'user_name',
            'phone',
            'role',
            'status',
            'is_pdf',
            'pdf_updated_at',
            'tests',
        ]
        read_only_fields = ['id', 'user', 'pdf_updated_at', 'role']

    def get_tests(self, obj):
        tests = obj.get_tests()        # ← TestResult queryset
        return TestResultSerializer(tests, many=True).data



class UserProfilePDFSerializer(serializers.ModelSerializer):
    """Сериализатор только для обновления is_pdf"""
    class Meta:
        model = UserProfile
        fields = ['is_pdf']
    
    def update(self, instance, validated_data):
        from django.utils import timezone
        instance.is_pdf = validated_data.get('is_pdf', instance.is_pdf)
        instance.pdf_updated_at = timezone.now()
        instance.save()
        return instance


class AdminUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ['id', 'name', 'phoneNumber', 'role', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class AdminUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ['id', 'name', 'phoneNumber', 'role', 'is_active', 'is_staff', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class AdminUserUpdateRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ['role']

    def validate_role(self, value):
        valid_roles = ['user', 'admin']
        if value not in valid_roles:
            raise serializers.ValidationError(f"Role must be one of {valid_roles}")
        return value


class TestAdminSerializer(serializers.ModelSerializer):
    userName = serializers.CharField(source="profile.user.name", read_only=True)
    status = serializers.SerializerMethodField()
    timeSpent = serializers.SerializerMethodField()

    class Meta:
        model = TestResult
        fields = [
            "id",
            "userName",
            "level",
            "dateCompleted",
            "timeSpent",
            "totalQuestions",
            "correctAnswers",
            "incorrectAnswers",
            "score",
            "status",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_status(self, obj):
        if obj.correctAnswers is None:
            return "not_started"
        if obj.score < 100 and obj.correctAnswers + obj.incorrectAnswers < obj.totalQuestions:
            return "in_progress"
        return "completed"

    @extend_schema_field(OpenApiTypes.STR)
    def get_timeSpent(self, obj):
        return "N/A"


class AdminRoleSerializer(serializers.ModelSerializer):
    """Сериализатор для управления администраторами"""
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})
    passwordConfirm = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})
    
    class Meta:
        model = AdminUser
        fields = [
            'id', 'name', 'phoneNumber', 'role', 'is_active', 
            'is_staff', 'date_joined', 'password', 'passwordConfirm'
        ]
        read_only_fields = ['id', 'date_joined']
        extra_kwargs = {
            'role': {'choices': ['admin', 'superadmin']}
        }
    
    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('passwordConfirm')
        
        if password or password_confirm:
            if not password or not password_confirm:
                raise serializers.ValidationError(
                    "Both password and password confirmation are required"
                )
            if password != password_confirm:
                raise serializers.ValidationError("Passwords do not match")
        
        if 'passwordConfirm' in data:
            del data['passwordConfirm']
        
        return data
    
    def validate_role(self, value):
        if value not in ['admin', 'superadmin']:
            raise serializers.ValidationError(
                "Role must be either 'admin' or 'superadmin'"
            )
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = AdminUser(**validated_data)
        
        if password:
            user.set_password(password)
        else:
            user.set_password('default123')
        
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance