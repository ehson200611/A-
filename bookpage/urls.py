from django.urls import path
from .views import (
    BookCreateView,
    BookListView,
    BookDetailView,
    BookUpdateView,
    BookDeleteView,
    ReadBookPDFView
)

urlpatterns = [
    path("", BookListView.as_view()),     
    path('<int:pk>/read/', ReadBookPDFView.as_view()),       # GET list
    path("create/", BookCreateView.as_view()),   # POST
    path("<int:pk>/", BookDetailView.as_view()), # GET one
    path("<int:pk>/update/", BookUpdateView.as_view()), # PUT/PATCH
    path("<int:pk>/delete/", BookDeleteView.as_view()), # DELETE
]
