from rest_framework import serializers
from .models import AdminUser, NotificationAdmin, AdminForSuperAdmin, TestAdmin

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = '__all__'

class NotificationAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationAdmin
        fields = '__all__'

class AdminForSuperAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminForSuperAdmin
        fields = '__all__'

class TestAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAdmin
        fields = '__all__'
