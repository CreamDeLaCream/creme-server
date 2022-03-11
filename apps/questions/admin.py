from django.contrib import admin

from .models import AnalysisNeed, Need, Question, QuestionChoice


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "question",
    )


@admin.register(QuestionChoice)
class QuestionChoiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "content",
    )


@admin.register(Need)
class NeedAdmin(admin.ModelAdmin):
    list_display = (
        "choice",
        "name",
        "description",
    )


@admin.register(AnalysisNeed)
class AnalysisNeedAdmin(admin.ModelAdmin):
    list_display = (
        "need",
        "analysis",
    )
