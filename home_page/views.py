from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import SwiperItem, Feature, Testimonial, Course, GalleryItem, Partner, Stat, WhyUsItem, InfoSwiperItem
from .serializers import (
    SwiperItemSerializer, FeatureSerializer, TestimonialSerializer,
    CourseSerializer, GalleryItemSerializer, PartnerSerializer,
    StatSerializer, WhyUsItemSerializer, InfoSwiperItemSerializer
)

class BaseViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]


class SwiperItemViewSet(viewsets.ModelViewSet):
    queryset = SwiperItem.objects.all().order_by('order')
    serializer_class = SwiperItemSerializer
    parser_classes = [MultiPartParser, FormParser] 


class FeatureViewSet(BaseViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    parser_classes = (MultiPartParser, FormParser)

class CourseViewSet(BaseViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class GalleryItemViewSet(BaseViewSet):
    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer

class PartnerViewSet(BaseViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    
from rest_framework.viewsets import ModelViewSet
from .models import Stat
from .serializers import StatSerializer

class StatViewSet(ModelViewSet):
    queryset = Stat.objects.all()
    serializer_class = StatSerializer


class WhyUsItemViewSet(BaseViewSet):
    queryset = WhyUsItem.objects.all()
    serializer_class = WhyUsItemSerializer

class InfoSwiperItemViewSet(BaseViewSet):
    queryset = InfoSwiperItem.objects.all()
    serializer_class = InfoSwiperItemSerializer
