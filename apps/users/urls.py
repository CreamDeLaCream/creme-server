from django.urls import path

from . import views

urlpatterns = [
    path("", views.UserAPIView.as_view()),
    path("keyword", views.UserKeywordListAPIView.as_view()),
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
    path("<pk>", views.UserLifeStyleAPIView.as_view()),
]
