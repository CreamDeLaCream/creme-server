import requests
from django.conf import settings
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenRefreshView,
    TokenVerifyView,
)

from .models import User, UserKeyword
from .serializers import UserKeywordSerializer, UserSerializer


class TokenAPIView(APIView):
    """
    Signup or Signin class
    """

    def get(self, request):
        # code를 통해 kakao access token 발급

        code = request.GET.get("code")
        client_id = getattr(settings, "KAKAO_REST_API_KEY")
        redirect_uri = "http://localhost:3000/users/kakao/callback"
        kakao_oauthurl = f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"  # noqa = E501

        # 인증코드를 토큰서버로 보내야함
        token_request = requests.get(kakao_oauthurl)
        # 보낸 요청에 대한 데이터(토큰)를 받음
        token_json = token_request.json()

        if "error" in token_json:
            return Response("에러가 발생했습니다!")

        access_token = token_json["access_token"]

        # 발급 받은 access_token을 통해 유저 이메일을 가져옴
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        data = profile_request.json()
        kakao_account = data["kakao_account"]
        email = kakao_account["email"]
        username = kakao_account["profile"]["nickname"]

        """
        Signup or Signin Request
        """

        try:
            user = User.objects.get(email=email)
            # 이미 kakao로 가입된 유저라면
            User.objects.filter(email=email).update(email=email, username=username)

        except User.DoesNotExist:
            # 기존에 가입된 유저가 없으면 새로 가입
            user = User.objects.filter(email=email).create(
                email=email, username=username
            )

        def get_tokens_for_user(user):
            refresh = RefreshToken.for_user(user)

            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

        tokens = get_tokens_for_user(user)

        response = Response(tokens, status=200)
        response.set_cookie(
            "access",
            value=tokens["access"],
            max_age=None,
            expires=None,
            path="/",
            domain=None,
            secure=False,
            httponly=False,
            samesite=None,
        )
        return response


class TokenBlacklistView(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserKeywordListAPIView(ListAPIView):
    """
    User Keyword List class
    """

    queryset = UserKeyword.objects.all()
    serializer_class = UserKeywordSerializer


class UserAPIView(APIView):
    """
    User class
    """

    # permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        access = request.COOKIES["access"]  # noqa : F841
        queryset = User.objects.get(email=request.user)
        username = queryset.username
        id = queryset.id
        user = {"username": username, "id": id}
        return Response(user)


class UserLifeStyleAPIView(RetrieveUpdateDestroyAPIView):
    """
    User Life style class
    """

    # permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer
