from rest_framework_simplejwt.authentication import JWTAuthentication


class MyJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # user, validated_token = super().authenticate(request)
        # if not user:
        access = request.COOKIES.get("access")
        # if access:
        validated_token = self.get_validated_token(access)
        return self.get_user(validated_token), validated_token

        # return user, validated_token
