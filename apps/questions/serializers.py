from rest_framework import serializers

from .models import Question, QuestionChoice


class QuestionChoiceSerializer(serializers.ModelSerializer):
    """질문 선택지"""

    class Meta:
        model = QuestionChoice
        fields = (
            "choice_index",
            "content",
        )


class QuestionSerializer(serializers.ModelSerializer):
    choice_index = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            "id",
            "question",
            "choice_index",
            "content",
        )

    def get_choice_index(self, obj):
        return obj.choice_index

    def get_content(self, obj):
        return obj.content


class ChoiceSolutionSerializer(serializers.ModelSerializer):
    """선택지별 솔루션"""

    class Meta:
        model = QuestionChoice
        fields = (
            "content",
            "solution",
        )
