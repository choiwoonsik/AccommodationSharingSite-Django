from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()

    pass


class PhotoInline(admin.TabularInline):

    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basci Info",
            {"fields": ("name", "description", "country", "city", "address", "price")},
        ),
        (
            "Times",
            {"fields": ("check_in", "check_out", "instant_book")},
        ),
        (
            "Spces",
            {
                "fields": (
                    "room_type",
                    "guests",
                    "beds",
                    "bedrooms",
                    "baths",
                )
            },
        ),
        (
            "More About the Spaces",
            {
                "classes": ("collapse",),
                "fields": (
                    "amenities",
                    "facilities",
                    "house_rules",
                ),
            },
        ),
        ("Last Details", {"fields": ("host",)}),
        # ("", {"fields": ()}),
    )

    list_display = (
        "name",
        "host",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "room_type",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_facilities",
        "count_rules",
        "count_photos",
        "total_rating",
    )

    ordering = ("price",)

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    raw_id_fields = ("host",)

    search_fields = ["^city", "^host__username"]

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    # self = RoomAdmin, obj = row
    def count_amenities(self, obj):
        return obj.amenities.count()

    count_amenities.short_description = "Amenities count"

    def count_facilities(self, obj):
        return obj.facilities.count()

    count_facilities.short_description = "Facilities count"

    def count_rules(self, obj):
        return obj.house_rules.count()

    count_rules.short_description = "House Rule count"

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo count"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f"<img width=40px src = {obj.file.url}/>")

    get_thumbnail.short_description = "Thumbnail"

