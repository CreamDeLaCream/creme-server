from rest_framework import serializers

from .models import Question, QuestionChoice


class QuestionChoiceSerializer(serializers.ModelSerializer):
    """질문 선택지"""

    class Meta:
        model = QuestionChoice
        fields = (
            "sort_order",
            "content",
        )


class QuestionSerializer(serializers.ModelSerializer):
    question_choices = QuestionChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            "id",
            "question",
            "question_choices",
        )


class ChoiceSolutionSerializer(serializers.ModelSerializer):
    """선택지별 솔루션"""

    class Meta:
        model = QuestionChoice
        fields = (
            "content",
            "solution",
        )
