import json
from datetime import date

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.analysis.models import Analysis, DogEmotion
from apps.questions.serializers import QuestionChoiceSerializer

from .apps import AnalysisConfig
from .choices import AnalysisStatusChoices, EmotionChoices

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

        # TODO: 요청받은 dog 요청한 회원과 연결되어있는지

        # 한국식나이 = 현재 년도 - 태어난 년도 + 1
        if dog is not None:
            validated_data["dog_age"] = dog.age
            validated_data["dog_name"] = dog.name

        analysis = Analysis.objects.create(**validated_data)

        try:

            # 첫번째 index - > 가장 높은 퍼센트 감정
            # 마지막 index - > 좌표
            deserialize_json = json.loads(
                AnalysisConfig.dog_ai_model.predict(analysis.image.path)
            )

            dog_emotion = deserialize_json[0]

            coordinate = deserialize_json[-1]
            coordinate_text = ",".join(
                str(x) for x in coordinate["prob"][0] + coordinate["prob"][1]
            )

            choice_emotion = EmotionChoices.get_emotion(dog_emotion["emotion"])

            emotion = DogEmotion.objects.get(emotion=choice_emotion)

            analysis.dog_emotion = emotion
            analysis.dog_emotion_percentage = dog_emotion["prob"] * 100.0
            analysis.dog_coordinate = coordinate_text
            analysis.status = AnalysisStatusChoices.UPLOAD
            analysis.save()

        except Exception as e:
            # logger.exception(e)
            # logger.debug("강아지 사진을 분석할 수 없음")
            print(e)
            print("강아지 사진을 분석할 수 없음")
            raise ValidationError("강아지 사진을 분석할 수 없습니다.")

        # TODO: 사람 감정분석 ( 사람 인식은 필수가 아니므로 exception raise 불 필요)

        return analysis


class AnalysisHumanSerializer(serializers.ModelSerializer):
    """감정 상태 분석 step 2 사람 답변"""

    class Meta:
        model = Analysis
        fields = ("answer",)


class AnalysisSerializer(serializers.ModelSerializer):
    solution = QuestionChoiceSerializer(many=True)

    class Meta:
        model = Analysis
        fields = "__all__"
