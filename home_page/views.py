from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet

from .models import (
    SwiperItem, Feature, WhyUsItem, Stat, Partner,
    Testimonial, GalleryItem, Course, InfoSwiperItem
)

from .serializers import (
    SwiperItemSerializer, FeatureSerializer, WhyUsSerializer,
    StatSerializer, PartnerSerializer, TestimonialSerializer,
    GallerySerializer, CourseSerializer, InfoSwiperSerializer
)
from rest_framework.permissions import AllowAny

class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]



class SwiperItemViewSet(ModelViewSet):
    queryset = SwiperItem.objects.all()
    serializer_class = SwiperItemSerializer


class FeatureViewSet(BaseViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

class WhyUsViewSet(BaseViewSet):
    queryset = WhyUsItem.objects.all()
    serializer_class = WhyUsSerializer

class StatViewSet(BaseViewSet):
    queryset = Stat.objects.all()
    serializer_class = StatSerializer

class PartnerViewSet(BaseViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

class TestimonialViewSet(BaseViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer

class GalleryViewSet(BaseViewSet):
    queryset = GalleryItem.objects.all()
    serializer_class = GallerySerializer

class CourseViewSet(BaseViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class InfoSwiperViewSet(BaseViewSet):
    queryset = InfoSwiperItem.objects.all()
    serializer_class = InfoSwiperSerializer
