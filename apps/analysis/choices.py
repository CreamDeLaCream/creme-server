from typing import Any

from django.db import models
from django.utils.translation import gettext as _

# class ChoicesRetriveValueMixin(object):
#     @classmethod
#     def get_key_from_value(cls, value: str) -> str:
#         """TextChoice value 값을 입력받아 key를 반환"""
#         value = value.lower()
#         for choice in cls.choices:
#             if choice[1].lower() == value:
#                 return choice[0]
#         return ""

#     @classmethod
#     def get_value_from_key(cls, key: str) -> str:
#         """TextChoice key 값을 입력받아 value를 반환"""
#         key = key.lower()
#         for choice in cls.choices:
#             if choice[0].lower() == key:
#                 return choice[1]
#         return ""


class EmotionChoices(models.TextChoices):
    UNKNOWN = "UN", _("unknown")
    ANGRY = "AG", _("angry")
    SCARED = "SC", _("scared")
    HAPPY = "HP", _("happy")
    SAD = "SD", _("sad")

    @staticmethod
    def get_emotion(text: str) -> Any:
        text = text.lower()
        # AI에서 보내는 값
        emotions = (
            ("angry", EmotionChoices.ANGRY),
            ("scared", EmotionChoices.SCARED),
            ("happy", EmotionChoices.HAPPY),
            ("sad", EmotionChoices.SAD),
        )

        for emotion in emotions:
            if text == emotion[0]:
                return emotion[1]

        return EmotionChoices.UNKNOWN


class AnalysisStatusChoices(models.TextChoices):
    UNKNOWN = "UN", _("unknown")
    UPLOAD = "UP", _("uploaded")
    COMPLETED = "CP", _("completed")
