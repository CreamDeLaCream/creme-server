# from django.shortcuts import render
from rest_framework.generics import ListAPIView

from .models import DogKeyword
from .serializers import DogKeywordSerializer


class DogKeywordListAPIView(ListAPIView):
    """
    DogKeyword List class
    """

    queryset = DogKeyword.objects.all()
    serializer_class = DogKeywordSerializer
