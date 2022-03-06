from typing import List

from django.db.models import QuerySet
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Dog, DogKeyword
from .serializers import DogKeywordSerializer, DogSerializer


class DogListAPIView(ListCreateAPIView):
    """
    Dog List class
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Dog.objects.filter(user=request.user.id)
        serializer = DogSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user.id
        serializer = DogSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data

            dog = Dog()
            dog.user_id = user
            dog.name = validated_data["name"]
            dog.birth = validated_data["birth"]
            dog.image = validated_data["image"]

            def _make_keywords_from_list(self, keyword_list: List[str]) -> QuerySet:

                qs = DogKeyword.objects.filter(name__in=keyword_list)
                return qs

            def validate_dog_keyword(self, value):
                keywords = self._make_keywords_from_list(value)
                return keywords

            def create(self, validated_data):
                keywords = validated_data.pop("dog_keyword")

                dog.dog_keyword.set(keywords)

            dog.save()
            return Response({"detail": "success create dog"})

        return Response(serializer.errors)


class DogAPIView(RetrieveUpdateDestroyAPIView):
    """
    Dog class
    """

    permission_classes = [IsAuthenticated]

    queryset = Dog.objects.all()
    serializer_class = DogSerializer


class DogKeywordListAPIView(ListAPIView):
    """
    Dog Keyword List class
    """

    queryset = DogKeyword.objects.all()
    serializer_class = DogKeywordSerializer
