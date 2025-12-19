from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.middleware.csrf import get_token
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from accounts.models import AuthToken
from accounts.utils import generate_access_token, generate_refresh_token, _hash_token, decode_token
from django.contrib.auth import get_user_model
import logging
logger = logging.getLogger(__name__)


def _cookie_kwargs():
    secure = not settings.DEBUG
    return {
        "httponly": True,
        "secure": secure,
        "samesite": "Lax",
        "path": "/",
    }


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"detail": "invalid_credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        roles = list(user.userrole_set.values_list("role__name", flat=True))
        access = generate_access_token(user, roles=roles)
        payload, refresh_raw = generate_refresh_token(user)
        resp = Response({"access_token": access, "user_id": user.id, "roles": roles})
        resp.set_cookie("access_token", access, max_age=15 * 60, **_cookie_kwargs())
        resp.set_cookie("refresh_token", refresh_raw, max_age=7 * 24 * 3600, **_cookie_kwargs())
        return resp


class RefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        raw = request.COOKIES.get("refresh_token")
        if not raw:
            return Response({"detail": "missing_refresh"}, status=status.HTTP_401_UNAUTHORIZED)
        hashed = _hash_token(raw)
        try:
            auth_token = AuthToken.objects.get(hashed_token=hashed)
        except AuthToken.DoesNotExist:
            return Response({"detail": "invalid_refresh"}, status=status.HTTP_401_UNAUTHORIZED)
        if auth_token.revoked_at or auth_token.expires_at <= timezone.now():
            return Response({"detail": "expired_or_revoked"}, status=status.HTTP_401_UNAUTHORIZED)
        auth_token.revoked_at = timezone.now()
        auth_token.save(update_fields=["revoked_at"])
        user = auth_token.user
        roles = list(user.userrole_set.values_list("role__name", flat=True))
        access = generate_access_token(user, roles=roles)
        payload, refresh_raw = generate_refresh_token(user, family_id=str(auth_token.family_id))
        resp = Response({"access_token": access})
        resp.set_cookie("access_token", access, max_age=15 * 60, **_cookie_kwargs())
        resp.set_cookie("refresh_token", refresh_raw, max_age=7 * 24 * 3600, **_cookie_kwargs())
        return resp


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        raw = request.COOKIES.get("refresh_token")
        if raw:
            hashed = _hash_token(raw)
            try:
                auth_token = AuthToken.objects.get(hashed_token=hashed)
                auth_token.revoked_at = timezone.now()
                auth_token.save(update_fields=["revoked_at"])
            except AuthToken.DoesNotExist:
                pass
        resp = Response({"detail": "ok"})
        resp.delete_cookie("access_token", path="/")
        resp.delete_cookie("refresh_token", path="/")
        return resp


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info("MeView user_id=%s", getattr(request.user, "id", None))
        user = request.user
        roles = list(user.userrole_set.values_list("role__name", flat=True))
        return Response({"id": user.id, "username": user.username, "email": user.email, "roles": roles})


class CsrfTokenView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = get_token(request)
        resp = Response({"csrfToken": token})
        resp.set_cookie("csrftoken", token, samesite="Lax", secure=not settings.DEBUG, path="/")
        return resp


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        User = get_user_model()
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        if not username or not password:
            return Response({"detail": "username_and_password_required"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"detail": "username_taken"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(username=username, email=email or "")
        user.set_password(password)
        user.save()
        roles = list(user.userrole_set.values_list("role__name", flat=True))
        access = generate_access_token(user, roles=roles)
        payload, refresh_raw = generate_refresh_token(user)
        resp = Response({"access_token": access, "user_id": user.id, "roles": roles})
        resp.set_cookie("access_token", access, max_age=15 * 60, httponly=True, secure=not settings.DEBUG, samesite="Lax", path="/")
        resp.set_cookie("refresh_token", refresh_raw, max_age=7 * 24 * 3600, httponly=True, secure=not settings.DEBUG, samesite="Lax", path="/")
        return resp
