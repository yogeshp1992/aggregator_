from django.contrib import admin  # noqa
from . import models

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

#
# # Define a new User admin
# class UserAdmin(BaseUserAdmin):
#     ordering = ("id",)
#     list_display = ("email", "name")


#  TODO - refer -
#  https://docs.djangoproject.com/en/4.1/topics/i18n/translation/
# https://docs.djangoproject.com/en/4.1/topics/i18n/translation/#internationalization-in-python-code
#  Required to globalize our project
#  Required for translation
from django.utils.translation import gettext_lazy as _

from . import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""

    ordering = ["id"]
    list_display = ["email", "name"]

    # TODO - reference
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Information"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Very Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(models.User, UserAdmin)
