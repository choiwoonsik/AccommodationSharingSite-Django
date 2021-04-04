from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# from rooms import models as room_models


# class RoomInline(admin.TabularInline):

#     model = room_models.Room


@admin.register(models.User)  # admin.site.register(models.User, CustomerUserAdmin)
class CustomerUserAdmin(UserAdmin):

    """ Customer User Admin """

    # inlines = (RoomInline,)

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
                    "login_method",
                    "email_verified",
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "id",
    )

    ordering = ("id",)

    list_display = (
        "username",
        "id",
        "first_name",
        "last_name",
        "email",
        "login_method",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
    )
