from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import FAQPage, FAQText
from .serializers import FAQPageSerializer, FAQTextSerializer


# 🔹 CRUD барои матни умумии FAQ (title, description ва ғайра)
class FAQTextListCreateView(generics.ListCreateAPIView):
    queryset = FAQText.objects.all()
    serializer_class = FAQTextSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="List or Create FAQText")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Create FAQText")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class FAQTextDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQText.objects.all()
    serializer_class = FAQTextSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Retrieve, Update or Delete FAQText")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# 🔹 CRUD барои саҳифаҳои FAQ (savol ва javob)
class FAQPageListCreateView(generics.ListCreateAPIView):
    queryset = FAQPage.objects.all()
    serializer_class = FAQPageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="List or Create FAQ Pages")
    def get(self, request, *args, **kwargs):
        """
        Ҳамаи саволҳо ва ҷавобҳои FAQ-ро бармегардонад.
        """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Create FAQ Page")
    def post(self, request, *args, **kwargs):
        """
        Саволи нав ва ҷавоби онро илова мекунад.
        """
        return super().post(request, *args, **kwargs)


class FAQPageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQPage.objects.all()
    serializer_class = FAQPageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Retrieve, Update or Delete one FAQ Page")
    def get(self, request, *args, **kwargs):
        """
        Яке аз FAQ-ҳоро бар асоси ID мегирад.
        """
        return super().get(request, *args, **kwargs)
