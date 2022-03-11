from django.urls import path

from . import views

urlpatterns = [
    path("keyword", views.DogKeywordListAPIView.as_view()),
    path("", views.DogListAPIView.as_view()),
    path("<pk>", views.DogAPIView.as_view()),
]
