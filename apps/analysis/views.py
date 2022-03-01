from rest_framework import parsers
from rest_framework.generics import CreateAPIView

from .models import Analysis
from .serializers import (
    AnalysisPersonSerializer,
    AnalysisPetSerializer,
    AnalysisSerializer,
)


class AnalysisPetView(CreateAPIView):
    """분석 step 1"""

    serializer_class = AnalysisPetSerializer
    queryset = Analysis.objects.all()
    parser_classes = (parsers.MultiPartParser,)
