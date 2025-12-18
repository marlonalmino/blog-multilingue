from django.conf import settings
from django.db import models
from django.db.models import Q
from django.contrib.postgres.search import SearchVectorField
import bleach


class Locale(models.TextChoices):
    PT = "pt", "pt"
    EN = "en", "en"
    ES = "es", "es"


class PostStatus(models.TextChoices):
    DRAFT = "draft", "draft"
    REVIEW = "review", "review"
    SCHEDULED = "scheduled", "scheduled"
    PUBLISHED = "published", "published"
    ARCHIVED = "archived", "archived"


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="posts")
    slug_base = models.SlugField(unique=True, max_length=255)
    status = models.CharField(max_length=20, choices=PostStatus.choices, default=PostStatus.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)
    cover_media = models.ForeignKey("media.MediaAsset", null=True, blank=True, on_delete=models.SET_NULL, related_name="cover_posts")
    canonical_url = models.URLField(max_length=500, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(status=PostStatus.PUBLISHED, published_at__isnull=False) | ~Q(status=PostStatus.PUBLISHED),
                name="post_published_requires_date",
            ),
        ]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["published_at"]),
            models.Index(fields=["is_featured"]),
        ]

    def __str__(self):
        return self.slug_base


class PostLocale(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="locales")
    locale = models.CharField(max_length=3, choices=Locale.choices)
    title = models.CharField(max_length=300)
    summary = models.TextField(blank=True)
    body_md = models.TextField()
    body_html = models.TextField()
    slug_locale = models.SlugField(max_length=255)
    seo_title = models.CharField(max_length=300, blank=True)
    seo_description = models.CharField(max_length=500, blank=True)
    og_title = models.CharField(max_length=300, blank=True)
    og_description = models.CharField(max_length=500, blank=True)
    og_image_media = models.ForeignKey("media.MediaAsset", null=True, blank=True, on_delete=models.SET_NULL, related_name="og_image_posts")
    reading_time_words = models.PositiveIntegerField(default=0)
    search_vector = SearchVectorField(null=True, editable=False)

    class Meta:
        unique_together = [
            ("post", "locale"),
        ]
        constraints = [
            models.UniqueConstraint(fields=["locale", "slug_locale"], name="unique_slug_per_locale"),
        ]
        indexes = [
            models.Index(fields=["locale"]),
            models.Index(fields=["slug_locale"]),
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return f"{self.post_id}:{self.locale}"

    def save(self, *args, **kwargs):
        allowed_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'strong', 'em', 'a', 'img', 'blockquote', 'code', 'pre', 'br']
        allowed_attrs = {'a': ['href', 'title', 'rel'], 'img': ['src', 'alt', 'title']}
        self.body_html = bleach.clean(self.body_html or "", tags=allowed_tags, attributes=allowed_attrs, strip=True)
        self.reading_time_words = len((self.body_md or "").split())
        super().save(*args, **kwargs)


class PostRevision(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="revisions")
    locale = models.CharField(max_length=3, choices=Locale.choices)
    diff_md = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="post_revisions")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["post", "locale"]),
            models.Index(fields=["created_at"]),
        ]
