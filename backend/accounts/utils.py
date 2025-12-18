import os
import uuid
import hashlib
import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from accounts.models import AuthToken, TokenType


def _now():
    return datetime.now(timezone.utc)


def _hash_token(raw):
    return hashlib.sha256(raw.encode()).hexdigest()


def generate_access_token(user, roles=None, minutes=15):
    payload = {
        "sub": str(user.id),
        "exp": _now() + timedelta(minutes=minutes),
        "iat": _now(),
        "roles": roles or [],
        "type": "access",
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def generate_refresh_token(user, days=7, family_id=None):
    jti = str(uuid.uuid4())
    family = family_id or str(uuid.uuid4())
    payload = {
        "sub": str(user.id),
        "exp": _now() + timedelta(days=days),
        "iat": _now(),
        "jti": jti,
        "family_id": family,
        "type": "refresh",
    }
    raw = str(uuid.uuid4()) + "." + str(uuid.uuid4())
    hashed = _hash_token(raw)
    AuthToken.objects.create(
        user=user,
        jti=jti,
        family_id=family,
        hashed_token=hashed,
        type=TokenType.REFRESH,
        expires_at=payload["exp"],
    )
    return payload, raw


def decode_token(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

