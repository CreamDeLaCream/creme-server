from django.urls import path

from .views import AnalysisHumanView, AnalysisPetView, AnalysisResultView

urlpatterns = [
    path("pet", AnalysisPetView.as_view()),
    path("human", AnalysisHumanView.as_view()),
    path("result", AnalysisResultView.as_view()),
]
