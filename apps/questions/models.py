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
