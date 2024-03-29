import json
import time

import cv2
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.analysis.models import Analysis, DogEmotion
from apps.dogs.serializers import DogSerializer
from apps.questions.serializers import NeedSerializer, QuestionChoiceSerializer

from .apps import AnalysisConfig
from .choices import AnalysisStatusChoices, EmotionChoices

start = time.time()

# from apps.questions.serializers import QuestionChoiceSerializer


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

            img = cv2.imread(analysis.image.path)
            human_analysis = (
                AnalysisConfig.human_ai_model.detect_emotion_for_single_frame(img)
            )
            print(human_analysis)

        except Exception as e:
            # logger.exception(e)
            # logger.debug("강아지 사진을 분석할 수 없음")
            print(e)
            print("강아지 사진을 분석할 수 없음")
            raise ValidationError("강아지 사진을 분석할 수 없습니다.")

        # TODO: 사람 감정분석 ( 사람 인식은 필수가 아니므로 exception raise 불 필요)

        print("2time :", time.time() - start)

        return analysis


class AnalysisHumanSerializer(serializers.ModelSerializer):
    """감정 상태 분석 step 2 사람 답변"""

    def update(self, instance, validated_data):
        self._check_editable(instance)

        # 완료 처리
        # instance.status = AnalysisStatusChoices.COMPLETED
        return super().update(instance, validated_data)

    def _check_editable(self, instance, raise_exception=True) -> bool:
        """분석 후 선택지를 고를 수 있는 상태인지 확인"""

        if instance.status == AnalysisStatusChoices.UPLOAD:
            return True

        if raise_exception:
            raise ValidationError({"detail": "분석을 수정할 수 없습니다."})

        return False

    class Meta:
        model = Analysis
        fields = ("answer",)


class AnalysisResultSerializer(serializers.ModelSerializer):

    human_emotion = serializers.CharField(source="get_human_emotion_display")
    dog_emotion = serializers.CharField(source="dog_emotion.get_emotion_display")
    status = serializers.CharField(source="get_status_display")

    # solution
    # answers = QuestionChoiceSerializer(source="answer", many=True, read_only=True)
    solution = serializers.SerializerMethodField("get_solution_serializer")

    dog = DogSerializer(read_only=True)
    needs = NeedSerializer(many=True, read_only=True)

    def get_solution_serializer(self, obj):
        serializer = QuestionChoiceSerializer(
            obj.answer, many=True, context={"user": obj.user, "dog_name": obj.dog_name}
        )
        return serializer.data

    def to_representation(self, instance):
        res = super().to_representation(instance)
        username = instance.user.username if instance.user else "반려인"
        dog_name = instance.dog_name

        description = instance.dog_emotion.description.format(
            username=username, dog_name=dog_name
        )
        res.update({"dog_emotion_description": description})
        return res

    class Meta:
        model = Analysis
        fields = (
            "created_at",
            "dog_name",
            "dog_age",
            "slug",
            "image",
            "dog",
            "dog_emotion",
            "dog_emotion_percentage",
            "dog_coordinate",
            "human_emotion",
            "human_emotion_percentage",
            "human_coordinate",
            "status",
            "chemistry_percentage",
            "is_dog_emotion_negative",
            "is_human_emotion_negative",
            "is_chemistry_negative",
            "solution",
            # "answers",
            "needs",
        )


class DogAnaylsisSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = (
            "slug",
            "is_favorite",
            "memo",
        )


class AnalysisCompletedSerializer(serializers.ModelSerializer):
    # solution = QuestionChoiceSerializer(many=True)

    human_emotion = serializers.CharField(source="get_human_emotion_display")
    dog_emotion = serializers.CharField(source="dog_emotion.get_emotion_display")
    status = serializers.CharField(source="get_status_display")

    # solution
    solution = QuestionChoiceSerializer(source="answer", many=True, read_only=True)

    dog = DogSerializer(read_only=True)
    needs = NeedSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        res = super().to_representation(instance)
        username = instance.user.username if instance.user else "반려인"
        dog_name = instance.dog_name

        description = instance.dog_emotion.description.format(
            username=username, dog_name=dog_name
        )
        res.update({"dog_emotion_description": description})
        return res

    class Meta:
        model = Analysis
        fields = (
            "created_at",
            "dog_name",
            "dog_age",
            "slug",
            "image",
            "dog",
            "dog_emotion",
            "dog_emotion_percentage",
            "human_emotion",
            "human_emotion_percentage",
            "status",
            "chemistry_percentage",
            "is_dog_emotion_negative",
            "is_human_emotion_negative",
            "is_chemistry_negative",
            "solution",
            "needs",
            "memo",
            "is_favorite",
        )


class DogAnalysisRecordListSerializer(serializers.ModelSerializer):

    dog_emotion = serializers.CharField(source="dog_emotion.get_emotion_display")

    class Meta:
        model = Analysis
        fields = (
            "created_at",
            "dog_name",
            "slug",
            "image",
            "dog_emotion",
            "is_favorite",
        )


class DogAnalysisRecordSerializer(serializers.ModelSerializer):

    dog_emotion = serializers.CharField(source="dog_emotion.get_emotion_display")
    status = serializers.CharField(source="get_status_display")

    dog = DogSerializer(read_only=True)

    class Meta:
        model = Analysis
        fields = (
            "created_at",
            "dog_name",
            "slug",
            "image",
            "dog",
            "dog_emotion",
            "status",
        )
