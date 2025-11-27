from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import AdminUser, NotificationAdmin, UserProfile
from tests.models import TestResult
from tests.serializers import TestResultSerializer


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
    tests = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['user', 'phone', 'tests']

    def get_tests(self, obj):
        results = TestResult.objects.filter(profile=obj)
        return TestResultSerializer(results, many=True).data


# Новые сериализаторы для управления пользователями
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