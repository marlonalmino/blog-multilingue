from django.db import models
from blog.models import Locale


class Category(models.Model):
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="children")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Category {self.pk}"


class CategoryLocale(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="locales")
    locale = models.CharField(max_length=3, choices=Locale.choices)
    name = models.CharField(max_length=200)
    slug_locale = models.SlugField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = [
            ("category", "locale"),
        ]
        constraints = [
            models.UniqueConstraint(fields=["locale", "slug_locale"], name="unique_category_slug_per_locale"),
        ]
        indexes = [
            models.Index(fields=["locale"]),
            models.Index(fields=["slug_locale"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.category_id}:{self.locale}"


class Tag(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tag {self.pk}"


class TagLocale(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="locales")
    locale = models.CharField(max_length=3, choices=Locale.choices)
    name = models.CharField(max_length=200)
    slug_locale = models.SlugField(max_length=255)

    class Meta:
        unique_together = [
            ("tag", "locale"),
        ]
        constraints = [
            models.UniqueConstraint(fields=["locale", "slug_locale"], name="unique_tag_slug_per_locale"),
        ]
        indexes = [
            models.Index(fields=["locale"]),
            models.Index(fields=["slug_locale"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.tag_id}:{self.locale}"


class PostCategory(models.Model):
    post = models.ForeignKey("blog.Post", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ("post", "category"),
        ]
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["post"]),
        ]


class PostTag(models.Model):
    post = models.ForeignKey("blog.Post", on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ("post", "tag"),
        ]
        indexes = [
            models.Index(fields=["tag"]),
            models.Index(fields=["post"]),
        ]


# Create your models here.
