from django.conf import settings
from django.db import models
from django.db.models import Q
import uuid


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ("user", "role"),
        ]
        indexes = [
            models.Index(fields=["role"]),
            models.Index(fields=["user"]),
        ]


class TokenType(models.TextChoices):
    REFRESH = "refresh", "refresh"


class AuthToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="auth_tokens")
    jti = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    family_id = models.UUIDField(default=uuid.uuid4, editable=False)
    hashed_token = models.CharField(max_length=256)
    type = models.CharField(max_length=20, choices=TokenType.choices, default=TokenType.REFRESH)
    expires_at = models.DateTimeField()
    revoked_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["expires_at"]),
            models.Index(fields=["revoked_at"]),
        ]
        constraints = [
            models.CheckConstraint(check=Q(expires_at__isnull=False), name="auth_token_expires_not_null"),
        ]


class OAuthProvider(models.TextChoices):
    GOOGLE = "google", "google"
    GITHUB = "github", "github"


class OAuthAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="oauth_accounts")
    provider = models.CharField(max_length=20, choices=OAuthProvider.choices)
    provider_uid = models.CharField(max_length=255, unique=True)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["provider"]),
            models.Index(fields=["user"]),
        ]


# Create your models here.
