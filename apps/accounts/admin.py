from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "is_active",)
    list_filter = ("is_admin", "is_active", "created_at")
    fieldsets = (
        ("Auth", {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_admin", "is_verified", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("email",)
    ordering = ("created_at",)


admin.site.register(User, CustomUserAdmin)
