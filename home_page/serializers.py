from rest_framework import serializers, viewsets, status


from .models import (
    SwiperItem, Feature, WhyUsItem, Stat, Partner, Testimonial, GalleryItem, Course, InfoSwiperItem
)

# =============================
# SERIALIZERS
# =============================

class SwiperItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwiperItem
        fields = '__all__'

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'

class WhyUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyUsItem
        fields = '__all__'

class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = '__all__'

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryItem
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class InfoSwiperSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoSwiperItem
        fields = '__all__'

