from django.urls import path

from . import views

urlpatterns = [
    path("", views.DogListAPIView.as_view()),
    path("<pk>", views.DogAPIView.as_view()),
    path("keyword", views.DogKeywordListAPIView.as_view()),
]
