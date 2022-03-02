from rest_framework import serializers

from .models import DogKeyword


class DogKeywordSerializer(serializers.ModelSerializer):
    """강아지 성격 키워드"""

    class Meta:
        model = DogKeyword
        fields = (
            "id",
            "name",
        )
