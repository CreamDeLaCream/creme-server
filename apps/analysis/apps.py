from django.apps import AppConfig

from creme_ai.dogemotion.dog_model import DogModel
# from creme_ai.humanemotion.human_model import RMN


class AnalysisConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.analysis"

    # human_ai_model = RMN()
    human_ai_model = None
    dog_ai_model = DogModel(
        "creme_ai/dogemotion/landmarkDetector.dat",
        "creme_ai/dogemotion/dogHeadDetector.dat",
        "creme_ai/dogemotion/classifierRotatedOn100Ratio90Epochs100.h5",
    )
