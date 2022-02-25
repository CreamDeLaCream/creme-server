from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedMixin


class Dog(TimeStampedMixin):

    name = models.CharField(verbose_name=_("dog name"), max_length=30)
    birth = models.DateTimeField(verbose_name=_("date of birth"))
    image = models.ImageField(verbose_name=_("dog image"))

    class Meta:
        verbose_name = _("dog")
        db_table = "dog"

    def __str__(self) -> str:
        return self.name
