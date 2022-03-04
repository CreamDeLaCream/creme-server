import cv2
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from numpy import generic
from rest_framework import generics, parsers
from rest_framework.generics import CreateAPIView, UpdateAPIView

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


class AnalysisHumanView(generics.UpdateAPIView):
    """분석 step 2"""

    def get_object(self):
        slug = self.request.query_params.get("slug", None)
        return get_object_or_404(Analysis, slug=slug)

    serializer_class = AnalysisHumanSerializer
