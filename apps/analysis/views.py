
import cv2
from django.http import HttpResponse

from creme_ai.dogemotion import dog_model
from creme_ai.humanemotion import human_model

from rest_framework import parsers
from rest_framework.generics import CreateAPIView

from .models import Analysis
from .serializers import (
    AnalysisPersonSerializer,
    AnalysisPetSerializer,
    AnalysisSerializer,
)


class AnalysisPetView(CreateAPIView):
    """분석 step 1"""

    serializer_class = AnalysisPetSerializer
    queryset = Analysis.objects.all()
    parser_classes = (parsers.MultiPartParser,)

def analysis_model(request):
    image_path = "sample image path"
    landmark_detector_path = "landmark detector path"
    dog_head_detector_path = "dog head detector path"
    model_path = "model path"

    model = dog_model.DogModel(
        landmark_detector_path, dog_head_detector_path, model_path
    )

    dog_result = model.predict(image_path)

    human_image_path = "humanemotion/image.png"
    img = cv2.imread(human_image_path)
    human_result = human_model.RMN().detect_emotion_for_single_frame(img)

    result = dog_result, human_result

    return HttpResponse(result)
