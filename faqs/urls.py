from django.urls import path
from .views import (
    FAQTextListCreateView,
    FAQTextDetailView,
    FAQPageListCreateView,
    FAQPageDetailView
)

urlpatterns = [

    # CRUD барои саволҳо ва ҷавобҳо
    path('pages/', FAQPageListCreateView.as_view(), name='faq_page_list_create'),
    path('pages/<int:pk>/', FAQPageDetailView.as_view(), name='faq_page_detail'),
]
