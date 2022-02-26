# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import QuestionChoice
from .serializers import QuestionSerializer


class QuestionListAPIView(APIView):
    """
    Question List class
    """

    def get(self, request):
        serializer = QuestionSerializer(QuestionChoice.objects.all(), many=True)
        return Response(serializer.data)
