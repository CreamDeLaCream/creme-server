from rest_framework import generics, mixins, parsers

from .models import Analysis
from .serializers import (
    AnalysisPersonSerializer,
    AnalysisPetSerializer,
    AnalysisSerializer,
)


class AnalysisPetView(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
):
    serializer_class = AnalysisPetSerializer
    queryset = Analysis.objects.all()
    parser_classes = (parsers.MultiPartParser,)

    def post(self, request, *args, **kwargs):
        """분석 step 1"""
        return self.create(request, *args, **kwargs)
