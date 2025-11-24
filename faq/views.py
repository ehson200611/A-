from rest_framework import viewsets
from faq.models import FaqText, FaqPage
from faq.serializers import FaqTextSerializer, FaqPageSerializer

class FaqTextViewSet(viewsets.ModelViewSet):
    queryset = FaqText.objects.all()
    serializer_class = FaqTextSerializer

class FaqPageViewSet(viewsets.ModelViewSet):
    queryset = FaqPage.objects.all()
    serializer_class = FaqPageSerializer
