from django.contrib import admin

from .models import Dog, DogKeyword


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )


@admin.register(DogKeyword)
class DogKeywordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
