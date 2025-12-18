from django.db import models


class EmbedProviderWhitelist(models.Model):
    domain = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=200)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.domain


class Embed(models.Model):
    post_locale = models.ForeignKey("blog.PostLocale", on_delete=models.CASCADE, related_name="embeds")
    provider_domain = models.ForeignKey(EmbedProviderWhitelist, on_delete=models.PROTECT, related_name="embeds")
    url = models.CharField(max_length=500)
    external_id = models.CharField(max_length=255, blank=True)
    position = models.PositiveIntegerField()
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["post_locale"]),
            models.Index(fields=["provider_domain"]),
            models.Index(fields=["position"]),
        ]


# Create your models here.
