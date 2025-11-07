from rest_framework import generics
from .models import HomePage
from .serializers import HomePageSerializer

class HomePageRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = HomePageSerializer

    def get_object(self):
        # Ҳамеша аввалин объекти HomePage-ро гиред
        obj, created = HomePage.objects.get_or_create(id=1, defaults={'data': {}})
        return obj
