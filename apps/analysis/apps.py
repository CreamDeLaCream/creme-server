from django.apps import AppConfig

from creme_ai.dogemotion.dog_model import DogModel
from creme_ai.humanemotion.human_model import RMN


class AnalysisConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.analysis"

    dog_ai_model = DogModel(
        "creme_ai/dogemotion/landmarkDetector.dat",
        "creme_ai/dogemotion/dogHeadDetector.dat",
        "creme_ai/dogemotion/ResNet50_LR00005_BS16_EP30_L2_newdata.h5",
    )
    human_ai_model = RMN()
