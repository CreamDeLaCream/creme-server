import cv2
from django.http import HttpResponse
from rest_framework import parsers
from rest_framework.generics import CreateAPIView

from creme_ai.dogemotion import dog_model
from creme_ai.humanemotion import human_model

from .models import Analysis
from .serializers import (
    AnalysisHumanSerializer,
    AnalysisPetSerializer,
    AnalysisSerializer,
)


class AnalysisPetView(CreateAPIView):
    """분석 step 1"""

    serializer_class = AnalysisPetSerializer
    queryset = Analysis.objects.all()
    parser_classes = (parsers.MultiPartParser,)


class AnalysisHumanView(CreateAPIView):
    """분석 step 2"""

    serializer_class = AnalysisHumanSerializer
    queryset = Analysis.objects.all()
