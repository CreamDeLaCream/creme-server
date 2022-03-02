from django.urls import path

from . import views

urlpatterns = [
    path("", views.DogKeywordListAPIView.as_view()),
]
