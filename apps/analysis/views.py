from django.shortcuts import get_object_or_404
from rest_framework import parsers
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)

from .models import Analysis
from .serializers import (
    AnalysisHumanSerializer,
    AnalysisPetSerializer,
    AnalysisResultSerializer,
    DogAnalysisRecordListSerializer,
    DogAnalysisRecordSerializer,
)


class AnalysisPetView(CreateAPIView):
    """분석 step 1"""

    serializer_class = AnalysisPetSerializer
    queryset = Analysis.objects.all()
    parser_classes = (parsers.MultiPartParser,)


class AnalysisHumanView(UpdateAPIView):
    """분석 step 2"""

    def get_object(self):
        slug = self.request.query_params.get("slug", None)
        return get_object_or_404(Analysis, slug=slug)

    serializer_class = AnalysisHumanSerializer


class AnalysisResultView(RetrieveAPIView):
    """분석 결과"""

    def get_object(self):
        slug = self.request.query_params.get("slug", None)
        return get_object_or_404(Analysis, slug=slug)

    serializer_class = AnalysisResultSerializer


class AllDogAnalysisRecordListAPIView(ListAPIView):
    """
    user의 모든 강아지 분석 기록
    """

    serializer_class = DogAnalysisRecordListSerializer

    def get_queryset(self):
        user = self.request.user.id
        return Analysis.objects.filter(user_id=user).order_by("-created_at")


class DogAnalysisRecordEmotionListAPIView(ListAPIView):
    """
    user의 모든 강아지 감정별 기록
    """

    serializer_class = DogAnalysisRecordListSerializer

    def get_queryset(self):
        user = self.request.user.id
        emotion = self.kwargs["emotion"]
        queryset = Analysis.objects.filter(user_id=user) & Analysis.objects.filter(
            dog_emotion_id=emotion
        )
        qs = queryset.order_by("-created_at")
        return qs


class DogAnalysisRecordAPIView(ListAPIView):
    """
    user의 강아지 id별 분석 기록
    """

    serializer_class = DogAnalysisRecordSerializer

    def get_queryset(self):
        user = self.request.user.id
        dog_id = self.kwargs["dogid"]
        queryset = Analysis.objects.filter(user_id=user) & Analysis.objects.filter(
            dog_id=dog_id
        )
        qs = queryset.order_by("-created_at")
        return qs


class DogAnalysisRecordEmotionAPIView(ListAPIView):
    """
    user의 강아지 id별 감정별 분석 기록
    """

    serializer_class = DogAnalysisRecordSerializer

    def get_queryset(self):
        user = self.request.user.id
        dog_id = self.kwargs["dogid"]
        emotion = self.kwargs["emotion"]
        queryset = (
            Analysis.objects.filter(user_id=user)
            & Analysis.objects.filter(dog_id=dog_id)
            & Analysis.objects.filter(dog_emotion_id=emotion)
        )
        qs = queryset.order_by("-created_at")
        return qs
