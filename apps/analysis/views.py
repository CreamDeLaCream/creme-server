# from django.shortcuts import render
import cv2
from django.http import HttpResponse

from creme_ai.dogemotion import dog_model
from creme_ai.humanemotion import human_model


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
