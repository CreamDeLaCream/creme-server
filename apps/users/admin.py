from django.contrib import admin

from .models import User, UserCharacter, UserKeyword


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
    )

    # manytomany field 추가 삭제
    filter_horizontal = ("user_keyword",)


admin.site.register(UserCharacter)


@admin.register(UserKeyword)
class UserKeywordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
