from django.db import models
from django.utils.translation import gettext as _


class ChoicesRetriveValueMixin(object):
    @classmethod
    def get_key_from_value(cls, value: str) -> str:
        """TextChoice value 값을 입력받아 key를 반환"""
        value = value.lower()
        for choice in cls.choices:
            if choice[1].lower() == value:
                return choice[0]
        return ""

    @classmethod
    def get_value_from_key(cls, key: str) -> str:
        """TextChoice key 값을 입력받아 value를 반환"""
        key = key.lower()
        for choice in cls.choices:
            if choice[0].lower() == key:
                return choice[1]
        return ""


class EmotionChoices(ChoicesRetriveValueMixin, models.TextChoices):
    UNKNOWN = "UN", _("unknown")
    ANGRY = "AG", _("angry")
    SCARED = "SC", _("scared")
    HAPPY = "HP", _("happy")
    SAD = "SD", _("sad")


class AnalysisStatusChoices(ChoicesRetriveValueMixin, models.TextChoices):
    UNKNOWN = "UN", _("unknown")
    UPLOAD = "UP", _("uploaded")
    COMPLETED = "CP", _("completed")
