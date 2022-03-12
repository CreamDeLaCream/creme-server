from rest_framework import parsers
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
    parser_classes = (parsers.MultiPartParser,)

    def get(self, request):
        queryset = Dog.objects.filter(user=request.user.id)
        serializer = DogSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = DogSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        dog = serializer.save()

        dog_keyword = request.data.get("dog_keyword")
        keyword_list = dog_keyword.split(",")
        keywords = DogKeyword.objects.filter(name__in=keyword_list)
        dog.dog_keyword.set(keywords)
        return Response(serializer.data)


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
