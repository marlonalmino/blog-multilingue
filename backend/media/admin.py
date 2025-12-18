from django.contrib import admin
from .models import MediaAsset, MediaVariant, MediaUsage


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ("id", "storage_provider", "path", "mime_type", "size_bytes", "created_at")
    list_filter = ("storage_provider", "mime_type")
    search_fields = ("path", "checksum")
    date_hierarchy = "created_at"


@admin.register(MediaVariant)
class MediaVariantAdmin(admin.ModelAdmin):
    list_display = ("id", "media", "format", "width", "height", "size_bytes", "created_at")
    list_filter = ("format",)
    search_fields = ("media__path",)


@admin.register(MediaUsage)
class MediaUsageAdmin(admin.ModelAdmin):
    list_display = ("media", "entity_type", "entity_id", "purpose")
    list_filter = ("entity_type", "purpose")
    search_fields = ("media__path",)

# Register your models here.
