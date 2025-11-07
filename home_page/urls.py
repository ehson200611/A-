from django.urls import path
from .views import HomePageRetrieveUpdateView

urlpatterns = [
    path('home-page/', HomePageRetrieveUpdateView.as_view(), name='home-page'),
]
