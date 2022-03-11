from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.analysis.choices import AnalysisStatusChoices, EmotionChoices
from apps.core.helper import generate_nanoid, get_uuid_path
from apps.core.models import TimeStampedMixin
from apps.dogs.models import Dog
from apps.questions.models import QuestionChoice


class DogEmotion(models.Model):

    emotion = models.CharField(
        verbose_name=_("emotion"),
        max_length=10,
        choices=EmotionChoices.choices,
        default=EmotionChoices.UNKNOWN,
    )
    description = models.TextField(verbose_name=_("description"))

    class Meta:
        verbose_name = _("dog emotion")
        db_table = "dog_emotion"

    def __str__(self) -> str:
        return EmotionChoices(self.emotion).label


class Analysis(TimeStampedMixin):

    dog_name = models.CharField(verbose_name=_("dog name"), max_length=10, blank=True)
    dog_age = models.IntegerField(verbose_name=_("dog age"), blank=True)

    slug = models.SlugField(
        verbose_name=_("analysis slug"),
        unique=True,
        default=generate_nanoid,
        max_length=40,
    )

    dog = models.ForeignKey(
        Dog, verbose_name=_("dog"), blank=True, null=True, on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        get_user_model(), null=True, blank=True, on_delete=models.CASCADE
    )
    answer = models.ManyToManyField(
        QuestionChoice,
        verbose_name=_("question choice"),
        related_name="analysis",
        blank=True,
    )

    image = models.ImageField(verbose_name=_("analysis image"), upload_to=get_uuid_path)

    dog_emotion = models.ForeignKey(
        DogEmotion, verbose_name=_("dog emotion"), null=True, on_delete=models.CASCADE
    )

    dog_emotion_percentage = models.DecimalField(
        verbose_name=_("dog emotion percentage"),
        default=0.0,
        max_digits=4,
        decimal_places=2,
    )

    dog_coordinate = models.CharField(
        verbose_name=_("dog coordinate"), blank=True, null=True, max_length=20
    )

    human_emotion = models.CharField(
        verbose_name=_("human emotion"),
        blank=True,
        null=True,
        max_length=10,
        choices=EmotionChoices.choices,
        default=EmotionChoices.UNKNOWN,
    )

    human_emotion_percentage = models.DecimalField(
        verbose_name=_("human emotion percentage"),
        default=0.0,
        max_digits=4,
        decimal_places=2,
    )

    human_coordinate = models.CharField(
        verbose_name=_("human coordinate"), blank=True, null=True, max_length=20
    )
    status = models.CharField(
        verbose_name=_("analysis status"),
        default=AnalysisStatusChoices.UNKNOWN,
        choices=AnalysisStatusChoices.choices,
        max_length=20,
    )
    chemistry_percentage = models.DecimalField(
        verbose_name=_("chemistry"), default=0.0, max_digits=5, decimal_places=2
    )

    needs = models.ManyToManyField(
        "questions.Need",
        through="questions.AnalysisNeed",
        through_fields=("analysis", "need"),
    )
    memo = models.TextField(verbose_name=_("memo"), blank=True)
    is_favorite = models.BooleanField(verbose_name=("is favorite"), default=False)

    @property
    def is_dog_emotion_negative(self) -> bool:
        return self.dog_emotion.emotion != EmotionChoices.HAPPY

    @property
    def is_human_emotion_negative(self) -> bool:
        return self.human_emotion != EmotionChoices.HAPPY

    @property
    def is_chemistry_negative(self) -> bool:
        sub = self.human_emotion_percentage - self.dog_emotion_percentage
        return (
            sub < 0
            if self.is_dog_emotion_negative == self.is_human_emotion_negative
            else sub > 0
        )

    class Meta:
        verbose_name = _("analysis")
        db_table = "analysis"

    def __str__(self) -> str:
        return _("{dog_name} analysis").format(dog_name=self.dog_name)


# [Deprecated] Analysis 모델과 통합
# class DogAnalysisRecord(TimeStampedMixin):
#     # user FK (django.contrib.auth -> get_user_model() 을 사용하여 모델을 가져온다)
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
#     analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE)
#     memo = models.TextField(verbose_name=_("memo"))

#     class Meta:
#         verbose_name = _("dog analysis record")
#         db_table = "dog_analysis_record"

#     def __str__(self) -> str:
#         return _("{username} {dog_name} analysis record").format(
#             username=self.user.username, dog_name=self.analysis.dog_name
#         )
