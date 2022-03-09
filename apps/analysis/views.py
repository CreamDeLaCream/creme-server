from django.shortcuts import get_object_or_404
from rest_framework import parsers
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.questions.models import Need, QuestionChoice

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
        serializer.save(
            user=self.request.user if not self.request.user.is_anonymous else None
        )


class AnalysisHumanView(GenericAPIView):
    """분석 step 2"""

    # permission_classes = [IsAuthenticated, AllowAny]

    serializer_class = AnalysisHumanSerializer

    def get_object(self):
        slug = self.request.query_params.get("slug", None)
        return get_object_or_404(Analysis, slug=slug)

    def post(self, request, *args, **kwargs):
        slug = request.data.get("slug")
        analysis = Analysis.objects.get(slug=slug)
        choices = []
        needs = []
        chemistry = 0
        for item in request.data["answer"]:
            choice_id = item["choice_id"]
            choices.append(choice_id)
            need = Need.objects.filter(choice=choice_id).first()
            needs.append(need)

        choice_instances = QuestionChoice.objects.filter(id__in=choices)

        # 같은 감정일때 /2
        if analysis.is_dog_emotion_negative == analysis.is_human_emotion_negative:
            chemistry += (
                analysis.human_emotion_percentage + analysis.dog_emotion_percentage
            ) / 2
        else:
            sub = analysis.human_emotion_percentage - analysis.dog_emotion_percentage
            # 사람 긍정
            # 강아지 부정
            chemistry += abs(sub)

        chemistry += sum(choice.increase_percentage for choice in choice_instances)

        analysis.chemistry_percentage = chemistry
        analysis.answer.set(choice_instances)
        analysis.needs.set(needs)

        serializer = AnalysisResultSerializer(instance=analysis)

        return Response(data=serializer.data)


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
