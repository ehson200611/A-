from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .models import *
from .serializers import *


class SwiperItemViewSet(viewsets.ModelViewSet):
    queryset = SwiperItem.objects.all()
    serializer_class = SwiperItemSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

class WhyUsViewSet(viewsets.ModelViewSet):
    queryset = WhyUsItem.objects.all()
    serializer_class = WhyUsSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

class StatViewSet(viewsets.ModelViewSet):
    queryset = Stat.objects.all()
    serializer_class = StatSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

class GalleryViewSet(viewsets.ModelViewSet):
    queryset = GalleryItem.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

class InfoSwiperViewSet(viewsets.ModelViewSet):
    queryset = InfoSwiperItem.objects.all()
    serializer_class = InfoSwiperSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]
