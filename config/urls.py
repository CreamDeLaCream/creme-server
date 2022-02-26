from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("apps.users.urls")),
    path("analysis/", include("apps.analysis.urls")),
    path("dogs/", include("apps.dogs.urls")),
    path("questions/", include("apps.questions.urls")),
]

# DEBUG일 떄 WAS에서 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
