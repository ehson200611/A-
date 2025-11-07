from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestPageViewSet

router = DefaultRouter()
router.register(r'home-page', TestPageViewSet, basename='testpage')

urlpatterns = [
    path('', include(router.urls)),
]
