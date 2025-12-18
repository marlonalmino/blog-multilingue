from django.contrib import admin
from .models import Comment, CommentModeration, PostReaction, CommentReaction


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "user", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("post__slug_base", "user__username", "user__email")
    date_hierarchy = "created_at"


@admin.register(CommentModeration)
class CommentModerationAdmin(admin.ModelAdmin):
    list_display = ("comment", "action", "performed_by", "created_at")
    list_filter = ("action",)
    search_fields = ("comment__id", "performed_by__username", "performed_by__email")
    date_hierarchy = "created_at"


@admin.register(PostReaction)
class PostReactionAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "type", "created_at")
    list_filter = ("type",)
    search_fields = ("post__slug_base", "user__username", "user__email")
    date_hierarchy = "created_at"


@admin.register(CommentReaction)
class CommentReactionAdmin(admin.ModelAdmin):
    list_display = ("comment", "user", "type", "created_at")
    list_filter = ("type",)
    search_fields = ("comment__id", "user__username", "user__email")
    date_hierarchy = "created_at"

# Register your models here.
