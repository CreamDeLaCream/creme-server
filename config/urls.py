from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

urlpatterns = [
    path("analysis/", include("apps.analysis.urls")),
    path("questions/", include("apps.questions.urls")),
    path("dogs/", include("apps.dogs.urls")),
]

if settings.DEBUG:
    # DEBUG일 떄 WAS에서 서빙
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    schema_view = get_schema_view(
        openapi.Info(
            title="Creme API Swagger",
            default_version="v1",
            description="CremeDeLaCreme API Document",
            terms_of_service="https://www.google.com/policies/terms/",
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
    )

    urlpatterns += [
        path("admin", RedirectView.as_view(url="admin/")),
        path("admin/", admin.site.urls),
        path("silk", RedirectView.as_view(url="silk/")),
        path("silk/", include("silk.urls", namespace="silk")),
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            r"^redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]
