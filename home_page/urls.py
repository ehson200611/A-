from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SwiperItemViewSet, FeatureViewSet, WhyUsViewSet, StatViewSet, PartnerViewSet,
    TestimonialViewSet, GalleryViewSet, CourseViewSet, InfoSwiperViewSet
)

router = DefaultRouter()

# ================================
# COMBINED IMAGE + TEXT ROUTES
# ================================
router.register(r'swiper', SwiperItemViewSet, basename='swiper')
router.register(r'feature', FeatureViewSet, basename='feature')
router.register(r'whyus', WhyUsViewSet, basename='whyus')
router.register(r'stat', StatViewSet, basename='stat')
router.register(r'partner', PartnerViewSet, basename='partner')
router.register(r'testimonial', TestimonialViewSet, basename='testimonial')
router.register(r'gallery', GalleryViewSet, basename='gallery')
router.register(r'course', CourseViewSet, basename='course')
router.register(r'infoswiper', InfoSwiperViewSet, basename='infoswiper')

urlpatterns = [
    path('', include(router.urls)),
]
