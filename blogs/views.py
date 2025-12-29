from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Blog
from .serializers import BlogSerializer
from .permissions import IsAdminOrReadOnly


# List/Create
class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAdminOrReadOnly]


# Retrieve/Update/Delete
class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAdminOrReadOnly]
