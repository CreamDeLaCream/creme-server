from django.shortcuts import get_object_or_404
from rest_framework import parsers
from rest_framework.generics import CreateAPIView, UpdateAPIView

from .models import Analysis
from .serializers import AnalysisHumanSerializer, AnalysisPetSerializer


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
