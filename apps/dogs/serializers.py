from rest_framework import serializers

from .models import Dog, DogKeyword


class DogSerializer(serializers.ModelSerializer):
    """강아지 정보"""

    dog_keyword = serializers.ListSerializer(
        child=serializers.CharField(max_length=20),
        required=False,
    )

    def create(self, validated_data):
        # list 를 가져옴
        dog = Dog.objects.create(**validated_data)
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
            "user",
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
