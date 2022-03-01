# from django.shortcuts import render
from rest_framework.generics import ListAPIView

from .models import Question
from .serializers import QuestionSerializer

# from rest_framework.response import Response


class QuestionListAPIView(ListAPIView):
    """
    Question List class
    """

    queryset = Question.objects.prefetch_related("question_choices").all()
    serializer_class = QuestionSerializer

    # permission_classes =
