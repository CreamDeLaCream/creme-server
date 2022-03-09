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


class DogAnalysisRecordListAPIView(ListAPIView):
    """
    Dog Analysis Record List class

    사용자 access token 보내주면 해당 사용자 모든 강아지 감정분석 자료 최신순
    """

    serializer_class = DogAnalysisRecordSerializer

    def get_queryset(self):
        user = self.request.user.id
        return Analysis.objects.filter(user_id=user).order_by("-created_at")
