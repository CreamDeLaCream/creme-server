from django.urls import path

from . import views

urlpatterns = [
    path("kakao/", views.kakao_login),
    path("kakao/callback/", views.kakao_callback),
    path(
        "logout",
        views.TokenBlacklistView.as_view(),
    ),
    path(
        "token/refresh",
        views.TokenRefreshView.as_view(),
    ),
    path(
        "token/verify",
        views.TokenVerifyView.as_view(),
    ),
]
