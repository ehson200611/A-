from rest_framework import serializers
from .models import VacancyUser

class VacancyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VacancyUser
        fields = "__all__"
