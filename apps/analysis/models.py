from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.helper import get_uuid_path
from apps.core.models import TimeStampedMixin
from apps.dogs.models import Dog
from apps.questions.models import QuestionChoice


class DogEmotion(models.Model):

    emotion = models.CharField(verbose_name=_("emotion"), max_length=10)
    description = models.TextField(verbose_name=_("emotion description"))

    class Meta:
        verbose_name = _("dog emotion")
        db_table = "dog_emotion"


class Analysis(TimeStampedMixin):

    dog_name = models.CharField(
        verbose_name=_("dog name"), max_length=10, blank=True, null=True
    )
    dog_age = models.IntegerField(verbose_name=_("dog age"), blank=True, null=True)

    slug = models.SlugField(verbose_name=_("analysis slug"), max_length=40, null=True)

    dog = models.ForeignKey(
        Dog, verbose_name=_("dog"), blank=True, null=True, on_delete=models.CASCADE
    )
    # slug default - > nanoid (생성할 떄 기본값으로 nanoid가 생성되게)

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
    dog_emotion_percentage = models.FloatField(
        verbose_name=_("dog emotion percentage"), blank=True, null=True
    )
    dog_coordinate = models.CharField(
        verbose_name=_("dog coordinate"), blank=True, null=True, max_length=20
    )
    human_emotion = models.CharField(
        verbose_name=_("human emotion"), blank=True, null=True, max_length=10
    )
    human_emotion_percentage = models.FloatField(
        verbose_name=_("human emotion percentage"), blank=True, null=True
    )
    human_coordinate = models.CharField(
        verbose_name=_("human coordinate"), blank=True, null=True, max_length=20
    )

    is_completed = models.BooleanField(
        verbose_name=_("analysis is completed"), default=False
    )

    class Meta:
        verbose_name = _("analysis")
        db_table = "analysis"


"""
    ---- 분석 요청 -----


    POST /api/analysis/pet
    content-type multipart
    request

    -----------------------
    dog_name: 강아지 이름

    -----------------------
    dog_age: 강아지 나이

    -----------------------
    dog(optional): fk id

    -----------------------
    image

    binary
    -----------------------

    response
    {
        slug: "fvJIFe_fF2",
    }

    ---- 질문 ----


    POST /api/analysis/person

    request
    {
        slug: "fvJIFe_fF2",
    }

"""


class DogAnalysisRecord(TimeStampedMixin):

    # user FK (django.contrib.auth -> get_user_model() 을 사용하여 모델을 가져온다)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE)
    memo = models.CharField(verbose_name=_("memo"), max_length=200)

    class Meta:
        verbose_name = _("dog analysis record")
        db_table = "dog_analysis_record"
