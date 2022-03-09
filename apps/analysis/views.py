from django.shortcuts import get_object_or_404
from rest_framework import parsers
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Analysis
from .serializers import (
    AnalysisHumanSerializer,
    AnalysisPetSerializer,
    AnalysisResultSerializer,
)


class AnalysisPetView(CreateAPIView):
    """분석 step 1"""

    serializer_class = AnalysisPetSerializer
    queryset = Analysis.objects.all()
    parser_classes = (parsers.MultiPartParser,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AnalysisHumanView(UpdateAPIView):
    """분석 step 2"""

    permission_classes = [IsAuthenticated, AllowAny]

    def get_object(self):
        slug = self.request.query_params.get("slug", None)
        return get_object_or_404(Analysis, slug=slug)

    serializer_class = AnalysisHumanSerializer


class AnaylsisQuestionChoiceView(GenericAPIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        return Response("dd")


class AnaylsisFavoriteView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        slug = request.data.get("slug")
        favorite = request.data.get("favorite", False)
        analysis = Analysis.objects.get(slug=slug)

        if analysis.user == request.user:
            analysis.is_favorite = favorite
            analysis.save()
        return Response(data=analysis.is_favorite)


class AnalysisResultView(RetrieveAPIView):
    """분석 결과"""

    def get_object(self):
        slug = self.request.query_params.get("slug", None)
        return get_object_or_404(Analysis, slug=slug)

    serializer_class = AnalysisResultSerializer
