from django.contrib import admin
from .models import ContentEvent, AuditLog


@admin.register(ContentEvent)
class ContentEventAdmin(admin.ModelAdmin):
    list_display = ("entity_type", "entity_id", "event", "created_at", "processed_at")
    list_filter = ("event", "entity_type")
    search_fields = ("entity_id",)
    date_hierarchy = "created_at"


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("actor", "action", "entity_type", "entity_id", "ip", "created_at")
    list_filter = ("action", "entity_type")
    search_fields = ("actor__username", "actor__email")
    date_hierarchy = "created_at"

# Register your models here.
