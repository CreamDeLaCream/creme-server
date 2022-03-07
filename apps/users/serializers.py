from typing import List

from django.db.models import QuerySet
from rest_framework import serializers

from .models import User, UserKeyword


class UserSerializer(serializers.ModelSerializer):
    """반려인 정보"""

    user_keyword = serializers.ListSerializer(
        child=serializers.CharField(max_length=20),
    )

    def _make_keywords_from_list(self, keyword_list: List[str]) -> QuerySet:

        qs = UserKeyword.objects.filter(name__in=keyword_list)
        return qs

    def validate_dog_keyword(self, value):
        keywords = self._make_keywords_from_list(value)
        return keywords

    def create(self, validated_data):
        # list 를 가져옴
        keywords = validated_data.pop("user_keyword")

        user = User.objects.create(**validated_data)
        user.user_keyword.set(keywords)
        return user

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "birth",
            "age",
            "user_keyword",
        )

        extra_kwargs = {
            "birth": {"write_only": True},
            "age": {"read_only": True},
        }


class UserKeywordSerializer(serializers.ModelSerializer):
    """반려인 성격 키워드"""

    class Meta:
        model = UserKeyword
        fields = ("name",)
