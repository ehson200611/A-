from rest_framework import routers
from django.urls import path, include
from .views import (
    SwiperItemViewSet, FeatureViewSet, WhyUsViewSet, StatViewSet,
    PartnerViewSet, TestimonialViewSet, GalleryViewSet, CourseViewSet,
    InfoSwiperViewSet
)

router = routers.DefaultRouter()
router.register("swiper", SwiperItemViewSet)

router.register(r'features', FeatureViewSet, basename='home-features')
router.register(r'why-us', WhyUsViewSet, basename='home-why-us')
router.register(r'stats', StatViewSet, basename='home-stats')
router.register(r'partners', PartnerViewSet, basename='home-partners')
router.register(r'testimonials', TestimonialViewSet, basename='home-testimonials')
router.register(r'gallery', GalleryViewSet, basename='home-gallery')
router.register(r'courses', CourseViewSet, basename='home-courses')
router.register(r'info-swiper', InfoSwiperViewSet, basename='home-info-swiper')

urlpatterns = [
    path('', include(router.urls)),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from rest_framework.routers import DefaultRouter
from .views import SwiperItemViewSet


