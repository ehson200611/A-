from django.urls import path
from .views import (
    FAQTextListCreateView,
    FAQTextDetailView,
    FAQPageListCreateView,
    FAQPageDetailView
)

urlpatterns = [
    # CRUD барои матни умумӣ
    path('text/', FAQTextListCreateView.as_view(), name='faq_text_list_create'),
    path('text/<int:pk>/', FAQTextDetailView.as_view(), name='faq_text_detail'),

    # CRUD барои саволҳо ва ҷавобҳо
    path('pages/', FAQPageListCreateView.as_view(), name='faq_page_list_create'),
    path('pages/<int:pk>/', FAQPageDetailView.as_view(), name='faq_page_detail'),
]
