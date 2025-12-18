from django.conf import settings
from django.db import models


class EntityType(models.TextChoices):
    POST = "post", "post"
    COMMENT = "comment", "comment"
    MEDIA = "media", "media"
    POST_LOCALE = "post_locale", "post_locale"


class ContentEventType(models.TextChoices):
    PUBLISH = "publish", "publish"
    UPDATE = "update", "update"
    DELETE = "delete", "delete"
    COMMENT_APPROVED = "comment_approved", "comment_approved"


class ContentEvent(models.Model):
    entity_type = models.CharField(max_length=20, choices=EntityType.choices)
    entity_id = models.PositiveBigIntegerField()
    event = models.CharField(max_length=30, choices=ContentEventType.choices)
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["entity_type", "entity_id"]),
            models.Index(fields=["event"]),
            models.Index(fields=["created_at"]),
        ]


class AuditAction(models.TextChoices):
    CREATE = "create", "create"
    UPDATE = "update", "update"
    DELETE = "delete", "delete"
    PUBLISH = "publish", "publish"
    SCHEDULE = "schedule", "schedule"
    LOGIN = "login", "login"


class AuditLog(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="audit_logs")
    action = models.CharField(max_length=20, choices=AuditAction.choices)
    entity_type = models.CharField(max_length=20, choices=EntityType.choices)
    entity_id = models.PositiveBigIntegerField()
    diff = models.JSONField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["action"]),
            models.Index(fields=["entity_type", "entity_id"]),
            models.Index(fields=["created_at"]),
        ]


# Create your models here.
