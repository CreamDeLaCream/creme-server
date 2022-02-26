from rest_framework import serializers

from apps.analysis.models import Analysis
from apps.questions.serializers import ChoiceSolutionSerializer

"""

Analysis
    - 감정 상태 분석 step 1 ( write )
        - 강아지 이름, 나이, 이미지
    - 감정 상태 분석 step 2 ( write )
        - question,
    - 분석결과 조회 ( read )

"""


class AnalysisPetSerializer(serializers.ModelSerializer):
    """감정 상태 분석 step 1 강아지 표정"""

    class Meta:
        Model = Analysis
        fields = (
            "dog_name",
            "dog_age",
            "image",
        )


class AnalysisPersonSerializer(serializers.ModelSerializer):
    """감정 상태 분석 step 2 사람 답변"""

    class Meta:
        Model = Analysis
        fields = ("answer",)


class AnalysisSerializer(serializers.ModelSerializer):
    solution = ChoiceSolutionSerializer(many=True)

    class Meta:
        model = Analysis
        fields = "__all__"
