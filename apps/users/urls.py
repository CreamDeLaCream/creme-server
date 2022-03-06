from django.urls import path

from . import views

urlpatterns = [
    path("kakao/callback", views.TokenAPIView.as_view()),
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
