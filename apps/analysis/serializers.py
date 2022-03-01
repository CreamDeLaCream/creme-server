from datetime import date

from rest_framework import serializers

from apps.analysis.models import Analysis
from apps.dogs.models import Dog
from apps.questions.serializers import QuestionChoiceSerializer

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
        model = Analysis
        fields = (
            "slug",
            "dog",
            "dog_name",
            "dog_age",
            "image",
        )
        read_only_fields = ("slug",)

        extra_kwargs = {
            "dog": {"write_only": True},
            # "dog_name": {"required": True},
            # "dog_age": {"required": True},
            "image": {"required": True},
        }

    def validate(self, attrs):

        # 회원일 경우 dog id 값 전송, 비회원일경우 dog_name, dog_age 필수

        if "dog" not in attrs and ("dog_name" not in attrs or "dog_age" not in attrs):
            raise serializers.ValidationError("dog 값이 전달되지 않았습니다.")

        return super().validate(attrs)

    def create(self, validated_data):

        dog = validated_data.get("dog")

        # TODO: 요청받은 dog 요청한 회원과 연결되어있는지 체크

        # 한국식나이 = 현재 년도 - 태어난 년도 + 1
        if dog is not None:
            validated_data["dog_age"] = date.today().year - dog.birth.year + 1
            validated_data["dog_name"] = dog.name

        analysis = Analysis.objects.create(**validated_data)

        # TODO: 분석 로직 ai 연결 필요

        return analysis


class AnalysisPersonSerializer(serializers.ModelSerializer):
    """감정 상태 분석 step 2 사람 답변"""

    class Meta:
        model = Analysis
        fields = ("answer",)


class AnalysisSerializer(serializers.ModelSerializer):
    solution = QuestionChoiceSerializer(many=True)

    class Meta:
        model = Analysis
        fields = "__all__"
