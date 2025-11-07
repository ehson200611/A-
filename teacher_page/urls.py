from rest_framework import routers
from django.urls import path, include
from .views import TeacherViewSet, TeachersPageViewSet

router = routers.DefaultRouter()
router.register(r'teachers', TeacherViewSet)
router.register(r'teachers-page', TeachersPageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
