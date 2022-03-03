from django.contrib import admin

from .models import Dog, DogCharacter, DogKeyword


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )

    # manytomany field 추가 삭제
    filter_horizontal = ("dog_keyword",)


admin.site.register(DogCharacter)


@admin.register(DogKeyword)
class DogKeywordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
