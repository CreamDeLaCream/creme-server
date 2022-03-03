from django.urls import path

from .views import AnalysisHumanView, AnalysisPetView

urlpatterns = [
    path("pet", AnalysisPetView.as_view()),
    path("human", AnalysisHumanView.as_view()),
]
