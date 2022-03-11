from rest_framework import serializers

from .models import Need, Question, QuestionChoice


class QuestionChoiceSerializer(serializers.ModelSerializer):
    """질문 선택지"""

    def to_representation(self, instance):
        res = super().to_representation(instance)
        user = self.context.get("user")
        dog_name = self.context.get("dog_name")

        username = user.username if user else "반려인"
        dog_name = dog_name

        description = instance.solution.format(username=username, dog_name=dog_name)
        res.update({"solution": description})
        return res

    class Meta:
        model = QuestionChoice
        fields = (
            "id",
            "sort_order",
            "content",
            "solution",
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


class NeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Need
        fields = (
            "choice",
            "name",
            "description",
        )
