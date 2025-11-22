from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VacancyUserViewSet

router = DefaultRouter()
router.register("vacancy-user", VacancyUserViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
