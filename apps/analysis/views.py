from django.shortcuts import get_object_or_404
from rest_framework import parsers, status
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.questions.models import Need, QuestionChoice

from .models import Analysis
from .serializers import (
    AnalysisCompletedSerializer,
    AnalysisHumanSerializer,
    AnalysisPetSerializer,
    AnalysisResultSerializer,
    DogAnalysisRecordListSerializer,
    DogAnalysisRecordSerializer,
    DogAnaylsisSaveSerializer,
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


class AnalysisResultView(RetrieveAPIView):
    """분석 결과"""

    def get_object(self):
        slug = self.request.query_params.get("slug", None)
        return get_object_or_404(Analysis, slug=slug)

    serializer_class = AnalysisResultSerializer


class AnaylsisSaveView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = DogAnaylsisSaveSerializer

    def get(self, request, *args, **kwargs):
        """
        분석 완료된 결과 (메모, 즐겨찾기까지) 조회
        """
        slug = self.request.query_params.get("slug", None)
        project = get_object_or_404(Analysis, slug=slug)
        serializer = AnalysisCompletedSerializer(project)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        분석 결과에 메모, 즐겨찾기 추가
        """

        slug = request.data.get("slug")
        favorite = request.data.get("favorite", False)
        memo = request.data.get("memo", False)
        analysis = Analysis.objects.get(slug=slug)

        if analysis.user == request.user:
            analysis.is_favorite = favorite
            analysis.memo = memo
            analysis.save()
            return Response({"detail": "메모 저장 완료"}, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class AnaylsisFavoriteView(GenericAPIView):
    """좋아요 수정"""

    # permission_classes = [IsAuthenticated]
    serializer_class = DogAnaylsisSaveSerializer

    def post(self, request, *args, **kwargs):

        slug = request.data.get("slug")
        favorite = request.data.get("favorite", False)
        analysis = Analysis.objects.get(slug=slug)

        if analysis.user == request.user:
            analysis.is_favorite = favorite
            analysis.save()
            return Response({"detail": "좋아요 수정 완료"}, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


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
