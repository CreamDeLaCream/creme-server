import requests
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenRefreshView,
    TokenVerifyView,
)

from .models import User

BASE_URL = "http://127.0.0.1:8000/"
KAKAO_CALLBACK_URI = BASE_URL + "users/kakao/callback/"


@api_view(["GET"])
def kakao_login(request):
    client_id = getattr(settings, "KAKAO_REST_API_KEY")
    redirect_uri = KAKAO_CALLBACK_URI
    kakao_oauthurl = f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"  # noqa=E501
    return redirect(kakao_oauthurl)


@api_view(["GET"])
def kakao_callback(request):
    code = request.GET.get("code")
    client_id = getattr(settings, "KAKAO_REST_API_KEY")
    redirect_uri = KAKAO_CALLBACK_URI
    kakao_oauthurl = f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"  # noqa=E501

    token_request = requests.get(kakao_oauthurl)
    token_json = token_request.json()

    if "error" in token_json:
        return Response("에러가 발생했습니다!")

    access_token = token_json["access_token"]

    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    data = profile_request.json()

    kakao_account = data["kakao_account"]
    email = kakao_account["email"]
    username = kakao_account["profile"]["nickname"]

    """
    Signup or Signin
    """

    try:
        user = User.objects.get(email=email)
        User.objects.filter(email=email).update(email=email, username=username)

        def get_tokens_for_user(user):
            refresh = RefreshToken.for_user(user)
            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

        tokens = get_tokens_for_user(user)
        return Response(tokens)

    except User.DoesNotExist:
        user = User.objects.create(email=email, username=username)

        def get_tokens_for_user(user):
            refresh = RefreshToken.for_user(user)
            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

        tokens = get_tokens_for_user(user)

        return Response(tokens)


class TokenBlacklistView(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
