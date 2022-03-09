from django.urls import path

from .views import (
    AnalysisHumanView,
    AnalysisPetView,
    AnalysisResultView,
    AnaylsisFavoriteView,
)

urlpatterns = [
    path("pet", AnalysisPetView.as_view()),
    path("human", AnalysisHumanView.as_view()),
    path("result", AnalysisResultView.as_view()),
    path("favorite", AnaylsisFavoriteView.as_view()),
]
