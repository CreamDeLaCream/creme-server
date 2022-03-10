from django.urls import path

from .views import (
    AllDogAnalysisRecordListAPIView,
    AnalysisHumanView,
    AnalysisPetView,
    AnalysisResultView,
    DogAnalysisRecordAPIView,
    DogAnalysisRecordEmotionAPIView,
    DogAnalysisRecordEmotionListAPIView,
    AnaylsisFavoriteView,
)

urlpatterns = [
    path("pet", AnalysisPetView.as_view()),
    path("human", AnalysisHumanView.as_view()),
    path("result", AnalysisResultView.as_view()),
    path("history", AllDogAnalysisRecordListAPIView.as_view()),
    path("history/emotion/<emotion>", DogAnalysisRecordEmotionListAPIView.as_view()),
    path("history/<dogid>", DogAnalysisRecordAPIView.as_view()),
    path(
        "history/emotion/<dogid>/<emotion>", DogAnalysisRecordEmotionAPIView.as_view()
    ),
    path("favorite", AnaylsisFavoriteView.as_view()),
]
