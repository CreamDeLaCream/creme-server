# from django.shortcuts import render
import datetime

from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Dog, DogKeyword
from .serializers import DogKeywordSerializer, DogSerializer


class DogListAPIView(ListCreateAPIView):
    """
    Dog List class
    """

    nowYear = datetime.datetime.now().strftime("%Y")

    queryset = Dog.objects.all()

    serializer_class = DogSerializer

    # TODO: permission_classes, Birth -> age


class DogAPIView(RetrieveUpdateDestroyAPIView):
    """
    Dog class
    """

    queryset = Dog.objects.all()
    serializer_class = DogSerializer

    # TODO: permission_classes


class DogKeywordListAPIView(ListAPIView):
    """
    Dog Keyword List class
    """

    queryset = DogKeyword.objects.all()
    serializer_class = DogKeywordSerializer
