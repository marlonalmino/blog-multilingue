from django.contrib import admin
from .models import Role, UserRole, AuthToken, OAuthAccount


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    list_filter = ("role",)
    search_fields = ("user__username", "user__email")


@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "expires_at", "revoked_at", "jti", "family_id")
    list_filter = ("type", "revoked_at")
    search_fields = ("user__username", "user__email", "jti")


@admin.register(OAuthAccount)
class OAuthAccountAdmin(admin.ModelAdmin):
    list_display = ("user", "provider", "provider_uid", "email_verified", "created_at")
    list_filter = ("provider", "email_verified")
    search_fields = ("provider_uid", "user__email")

# Register your models here.
