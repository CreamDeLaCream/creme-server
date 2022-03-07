# 참고: https://docs.djangoproject.com/ko/4.0/ref/contrib/admin/

from django.contrib import admin

from .models import Analysis, DogAnalysisRecord, DogEmotion


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "dog_name",
    )
    # manytomany field 추가 삭제
    filter_horizontal = ("answer",)


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
