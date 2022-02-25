from django.contrib import admin

from .models import Analysis, DogAnalysisRecord, DogEmotion


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "dog_name",
    )


@admin.register(DogAnalysisRecord)
class DogAnalysisRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
    )


@admin.register(DogEmotion)
class DogEmotionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "emotion",
    )
