from ast import keyword

from django.db import models
from django.utils.translation import gettext_lazy as _


class Question(models.Model):

    question = models.TextField(verbose_name=_("question"))

    class Meta:
        verbose_name = _("question")
        db_table = "question"

    def __str__(self):
        return self.question


class QuestionChoice(models.Model):
    question = models.ForeignKey(
        Question,
        verbose_name=_("question"),
        related_name="question_choices",
        on_delete=models.CASCADE,
    )
    sort_order = models.IntegerField(verbose_name=_("question choice order"))
    content = models.TextField(verbose_name=_("question choice content"))
    solution = models.TextField(verbose_name=_("question choice solution"))

    increase_percentage = models.DecimalField(
        verbose_name=_("rate of increase"), default=0.0, max_digits=3, decimal_places=2
    )

    class Meta:
        verbose_name = _("question choice")
        db_table = "question_choice"

        constraints = [
            models.UniqueConstraint(
                fields=["question", "sort_order"], name="unique question choice"
            )
        ]


class Need(models.Model):

    choice = models.ForeignKey("questions.QuestionChoice", on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_("keyword"), max_length=30)
    description = models.TextField(verbose_name=_("description"))

    class Meta:
        verbose_name = _("necessary")
        db_table = "need"


class AnalysisNeed(models.Model):

    question = models.ForeignKey("questions.Need", on_delete=models.CASCADE)
    analysis = models.ForeignKey("analysis.Analysis", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("analysis need")
        db_table = "analysis_need"
