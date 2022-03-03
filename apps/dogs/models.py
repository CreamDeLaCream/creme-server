import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedMixin


class DogKeyword(models.Model):

    name = models.CharField(verbose_name=_("dog character keyword"), max_length=10)

    class Meta:
        verbose_name = _("dog keyword")
        db_table = "dog_keyword"

    def __str__(self):
        return self.name


class Dog(TimeStampedMixin):

    name = models.CharField(verbose_name=_("dog name"), max_length=30)
    birth = models.DateField(verbose_name=_("date of birth"))
    image = models.ImageField(verbose_name=_("dog image"), blank=True, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    dog_keyword = models.ManyToManyField(
        DogKeyword,
        through="DogCharacter",
        through_fields=("dog", "dog_keyword"),
    )

    @property
    def age(self) -> int:
        """강아지 나이를 반환합니다."""

        now_year = datetime.date.today().year
        dog_born_year = self.birth.year

        return now_year - dog_born_year + 1

    class Meta:
        verbose_name = _("dog")
        db_table = "dog"


class DogCharacter(models.Model):

    dog = models.ForeignKey(
        "dogs.Dog",
        verbose_name=_("dog"),
        on_delete=models.CASCADE,
    )

    dog_keyword = models.ForeignKey(
        "dogs.DogKeyword",
        on_delete=models.CASCADE,
        verbose_name=_("dog keyword"),
    )

    class Meta:
        verbose_name = _("dog character")
        db_table = "dog_character"
