from typing import List

from django.db.models import QuerySet
from rest_framework import serializers

from .models import Dog, DogKeyword


class DogSerializer(serializers.ModelSerializer):
    """강아지 정보"""

    dog_keyword = serializers.ListSerializer(
        child=serializers.CharField(max_length=20),
    )

    def _make_keywords_from_list(self, keyword_list: List[str]) -> QuerySet:

        qs = DogKeyword.objects.filter(name__in=keyword_list)
        return qs

    def validate_dog_keyword(self, value):
        keywords = self._make_keywords_from_list(value)
        return keywords

    def create(self, validated_data):
        # list 를 가져옴
        keywords = validated_data.pop("dog_keyword")

        dog = Dog.objects.create(**validated_data)
        dog.dog_keyword.set(keywords)
        return dog

    class Meta:
        model = Dog
        fields = (
            "id",
            "name",
            "birth",
            "age",
            "dog_keyword",
            "image",
            # "user",
        )
        # https://www.django-rest-framework.org/api-guide/fields/#core-arguments 참고
        extra_kwargs = {
            "birth": {"write_only": True},
            "age": {"read_only": True},
        }


class DogKeywordSerializer(serializers.ModelSerializer):
    """강아지 성격 키워드"""

    class Meta:
        model = DogKeyword
        fields = ("name",)
