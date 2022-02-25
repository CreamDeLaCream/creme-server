from django.contrib import admin

from .models import Question, QuestionChoice


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
