from django.urls import path

from .views import AnalysisPetView

urlpatterns = [
    path("pet", AnalysisPetView.as_view()),
]
