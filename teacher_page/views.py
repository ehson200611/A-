from rest_framework import viewsets
from .models import Teacher, TeachersPage
from .serializers import TeacherSerializer, TeachersPageSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class TeachersPageViewSet(viewsets.ModelViewSet):
    queryset = TeachersPage.objects.all()
    serializer_class = TeachersPageSerializer
