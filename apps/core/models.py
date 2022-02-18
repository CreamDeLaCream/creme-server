from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


class TimeStampedMixin(models.Model):
    """
    생성, 수정 날짜 필드를 포함하는 추상 모델
    """

    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        db_index=True,
        default=timezone.now,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updated at"),
        auto_now=True,
    )

    class Meta:
        abstract = True
