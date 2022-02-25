from django.db import models
from django.utils.translation import gettext_lazy as _


class Question(models.Model):

    question = models.TextField(verbose_name=_("question"))

    class Meta:
        verbose_name = _("question")
        db_table = "question"


class QuestionChoice(models.Model):

    choice_index = models.IntegerField(verbose_name=_("index"))
    content = models.TextField(verbose_name=_("question choice content"))
    solution = models.TextField(verbose_name=_("question choice solution"))

    class Meta:
        verbose_name = _("question choice")
        db_table = "question_choice"
