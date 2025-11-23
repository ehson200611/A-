from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VacancyUserViewSet,VacancyQuestionViewSet

router = DefaultRouter()
router.register("vacancy-user", VacancyUserViewSet)
router.register(r'vacancy-questions', VacancyQuestionViewSet, basename='vacancy-question')
urlpatterns = [
    path("", include(router.urls)),
]
