from django.contrib import admin
from .models import Category, CategoryLocale, Tag, TagLocale, PostCategory, PostTag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "parent", "created_at")
    search_fields = ("id",)


@admin.register(CategoryLocale)
class CategoryLocaleAdmin(admin.ModelAdmin):
    list_display = ("category", "locale", "name", "slug_locale")
    list_filter = ("locale",)
    search_fields = ("name", "slug_locale")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")
    search_fields = ("id",)


@admin.register(TagLocale)
class TagLocaleAdmin(admin.ModelAdmin):
    list_display = ("tag", "locale", "name", "slug_locale")
    list_filter = ("locale",)
    search_fields = ("name", "slug_locale")


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ("post", "category")
    search_fields = ("post__slug_base",)


@admin.register(PostTag)
class PostTagAdmin(admin.ModelAdmin):
    list_display = ("post", "tag")
    search_fields = ("post__slug_base",)

# Register your models here.
