from django.db import models


class StorageProvider(models.TextChoices):
    LOCAL = "local", "local"
    S3 = "s3", "s3"
    GCS = "gcs", "gcs"


class MediaAsset(models.Model):
    storage_provider = models.CharField(max_length=20, choices=StorageProvider.choices, default=StorageProvider.LOCAL)
    path = models.CharField(max_length=500)
    mime_type = models.CharField(max_length=100)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    checksum = models.CharField(max_length=64, unique=True)
    size_bytes = models.PositiveBigIntegerField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["mime_type"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.path


class VariantFormat(models.TextChoices):
    WEBP = "webp", "webp"
    AVIF = "avif", "avif"
    JPG = "jpg", "jpg"
    PNG = "png", "png"


class MediaVariant(models.Model):
    media = models.ForeignKey(MediaAsset, on_delete=models.CASCADE, related_name="variants")
    format = models.CharField(max_length=10, choices=VariantFormat.choices)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    size_bytes = models.PositiveBigIntegerField(null=True, blank=True)
    url = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["format"]),
            models.Index(fields=["width", "height"]),
        ]


class MediaEntityType(models.TextChoices):
    POST = "post", "post"
    POST_LOCALE = "post_locale", "post_locale"
    COMMENT = "comment", "comment"


class MediaPurpose(models.TextChoices):
    COVER = "cover", "cover"
    INLINE = "inline", "inline"
    OG = "og", "og"


class MediaUsage(models.Model):
    media = models.ForeignKey(MediaAsset, on_delete=models.CASCADE, related_name="usages")
    entity_type = models.CharField(max_length=20, choices=MediaEntityType.choices)
    entity_id = models.PositiveBigIntegerField()
    purpose = models.CharField(max_length=20, choices=MediaPurpose.choices)

    class Meta:
        unique_together = [
            ("media", "entity_type", "entity_id", "purpose"),
        ]
        indexes = [
            models.Index(fields=["entity_type", "entity_id"]),
            models.Index(fields=["purpose"]),
        ]


# Create your models here.
