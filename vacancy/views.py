from rest_framework.viewsets import ModelViewSet
from .models import VacancyUser
from .serializers import VacancyUserSerializer

class VacancyUserViewSet(ModelViewSet):
    queryset = VacancyUser.objects.all()
    serializer_class = VacancyUserSerializer
