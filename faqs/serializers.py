from rest_framework import serializers
from .models import FAQPage, FAQText


class FAQTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQText
        fields = "__all__"


class FAQPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQPage
        fields = "__all__"
