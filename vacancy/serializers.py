# serializers.py
from rest_framework import serializers
from .models import VacancyUser

class VacancyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VacancyUser
        fields = "__all__"


from rest_framework import serializers
from .models import VacancyQuestion

class VacancyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VacancyQuestion
        fields = "__all__"
