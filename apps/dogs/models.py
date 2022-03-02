from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedMixin


class Dog(TimeStampedMixin):

    name = models.CharField(verbose_name=_("dog name"), max_length=30)
    birth = models.DateTimeField(verbose_name=_("date of birth"))
    image = models.ImageField(verbose_name=_("dog image"))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("dog")
        db_table = "dog"

    def __str__(self) -> str:
        return self.name


class DogKeyword(models.Model):

    name = models.CharField(verbose_name=_("dog character keyword"), max_length=10)

    class Meta:
        verbose_name = _("dog keyword")
        db_table = "dog_keyword"
