from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)  # admin.site.register(models.User, CustomerUserAdmin)
class CustomerUserAdmin(UserAdmin):

    """ Customer User Admin """

    fieldsets = UserAdmin.fieldsets + (
        (
            "custom profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )
