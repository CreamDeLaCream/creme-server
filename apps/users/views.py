import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenRefreshView,
    TokenVerifyView,
)

from .models import User


class TokenAPIView(APIView):
    """
    Signup or Signin class
    """

    def post(self, request):
        token_json = request.json()

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

        email = request.email
        username = request.username
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
