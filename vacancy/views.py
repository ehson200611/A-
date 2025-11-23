# views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from .models import VacancyUser
from .serializers import VacancyUserSerializer

class VacancyUserViewSet(ModelViewSet):
    queryset = VacancyUser.objects.all()
    serializer_class = VacancyUserSerializer
    parser_classes = [MultiPartParser, FormParser]  # 👈 барои FormData ва file


from rest_framework.viewsets import ModelViewSet
from .models import VacancyQuestion
from .serializers import VacancyQuestionSerializer

class VacancyQuestionViewSet(ModelViewSet):
    queryset = VacancyQuestion.objects.all()
    serializer_class = VacancyQuestionSerializer

