from django.contrib import admin
from .models import EmbedProviderWhitelist, Embed


@admin.register(EmbedProviderWhitelist)
class EmbedProviderWhitelistAdmin(admin.ModelAdmin):
    list_display = ("domain", "name", "enabled", "created_at")
    list_filter = ("enabled",)
    search_fields = ("domain", "name")


@admin.register(Embed)
class EmbedAdmin(admin.ModelAdmin):
    list_display = ("post_locale", "provider_domain", "position", "url", "created_at")
    list_filter = ("provider_domain",)
    search_fields = ("url",)

# Register your models here.
