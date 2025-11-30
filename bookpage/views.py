from django.http import FileResponse, HttpResponseForbidden
from rest_framework import generics
from rest_framework.views import APIView
from .models import Book
from .serializers import BookSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# ---------- CREATE ----------
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @swagger_auto_schema(
        operation_description="Create book with PDF",
        consumes=["multipart/form-data"],
        manual_parameters=[
            openapi.Parameter("title", openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter("pdf", openapi.IN_FORM, type=openapi.TYPE_FILE),
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# ---------- LIST ----------
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# ---------- RETRIEVE ----------
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# ---------- UPDATE ----------
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @swagger_auto_schema(
        operation_description="Update book",
        consumes=["multipart/form-data"],
        manual_parameters=[
            openapi.Parameter("title", openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter("pdf", openapi.IN_FORM, type=openapi.TYPE_FILE),
        ],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update book",
        consumes=["multipart/form-data"],
        manual_parameters=[
            openapi.Parameter("title", openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter("pdf", openapi.IN_FORM, type=openapi.TYPE_FILE),
        ],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


# ---------- DELETE ----------
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer



class ReadBookPDFView(APIView):

    @swagger_auto_schema(
        operation_description="Read PDF inline (no download)",
        manual_parameters=[
            openapi.Parameter(
                name='pk', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER,
                description="ID of the book"
            )
        ],
        responses={200: "PDF file"},
    )
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Нет доступа")

        book = Book.objects.get(pk=pk)
        return FileResponse(open(book.pdf.path, "rb"), content_type="application/pdf")