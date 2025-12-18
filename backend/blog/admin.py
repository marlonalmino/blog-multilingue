from django.contrib import admin
from .models import Post, PostLocale, PostRevision


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("slug_base", "status", "published_at", "is_featured", "author")
    list_filter = ("status", "is_featured")
    search_fields = ("slug_base",)
    date_hierarchy = "published_at"


@admin.register(PostLocale)
class PostLocaleAdmin(admin.ModelAdmin):
    list_display = ("post", "locale", "title", "slug_locale")
    list_filter = ("locale",)
    search_fields = ("title", "slug_locale")


@admin.register(PostRevision)
class PostRevisionAdmin(admin.ModelAdmin):
    list_display = ("post", "locale", "created_by", "created_at")
    list_filter = ("locale",)
    date_hierarchy = "created_at"

# Register your models here.
