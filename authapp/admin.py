from django.contrib import admin
from authapp.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from events.models import *
from notifications.models import *


class UserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "is_staff", "is_active", "mobile", "role")
    list_filter = ("is_staff", "is_active")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password", "role", "profile_picture")}),
        (
            "Permissions",
            {
                "fields": (
                    "mobile",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "profile_picture",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "role",
                ),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # User is being created
            password = form.cleaned_data.get("password1")
            if password:
                obj.set_password(password)  # Hash the password
        super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)
admin.site.register(OTP)
admin.site.register(UserToken)
admin.site.register(Organizer)
admin.site.register(BankAccount)
