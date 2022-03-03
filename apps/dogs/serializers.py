from rest_framework import serializers

from .models import Dog, DogKeyword


class DogSerializer(serializers.ModelSerializer):
    """강아지 정보"""

    class Meta:
        model = Dog
        fields = (
            "id",
            "name",
            "birth",
            "image",
        )


class DogKeywordSerializer(serializers.ModelSerializer):
    """강아지 성격 키워드"""

    class Meta:
        model = DogKeyword
        fields = (
            "id",
            "name",
        )
