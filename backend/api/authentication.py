from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
from accounts.utils import decode_token
from django.contrib.auth import get_user_model


class JWTCookieAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get("Authorization")
        token = None
        if auth and auth.lower().startswith("bearer "):
            token = auth.split(" ", 1)[1].strip()
        else:
            token = request.COOKIES.get("access_token")
        if not token:
            return None
        try:
            payload = decode_token(token)
        except Exception:
            raise exceptions.AuthenticationFailed("Invalid token")
        if payload.get("type") != "access":
            raise exceptions.AuthenticationFailed("Invalid token type")
        User = get_user_model()
        try:
            user = User.objects.get(id=payload.get("sub"))
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found")
        return (user, None)
