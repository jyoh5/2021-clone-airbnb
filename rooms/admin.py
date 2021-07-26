from django.contrib import admin
from django.utils.html import mark_safe
from . import models


# Register your models here.(admin panel에 등록하겠다는 뜻)
@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    list_display = (
        "name",
        "used_by",
    )

    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """Photo Admin Definition"""

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f"<img style='width:50px;'src='{obj.file.url}' / >")

    get_thumbnail.short_description = "Thumbnail "


class PhotoInline(admin.TabularInline):
    # class PhotoInline(admin.StackedInline): # TabularInline와 모양만 다를 뿐...
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """Room Admin Definition"""

    inlines = (PhotoInline,)

    # admin 외부 화면 =================================
    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "address", "price")},
        ),
        (
            "Times",
            {"fields": ("check_in", "check_out", "instant_book")},
        ),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        (
            "More About the Space",
            {
                # "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        ("Last Details", {"fields": ("host",)}),
    )

    # admin 내부 화면 =================================
    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    # count_photo.short_description = "count_photo"

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

    # fields = ("country",)

    search_fields = ["=city", "host__username"]

    #  models.ManyToManyField(다대다 관계에서만 사용 가능)
    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    ordering = ("name", "price", "bedrooms")

    raw_id_fields = ("host",)

    # self = Admin class, obj = 1 row, 정렬 불가
    def count_amenities(self, obj):
        return obj.amenities.count()

    # count_amenities.short_description = "count_amenities"

    def count_photos(self, obj):
        return obj.photos.count()
        # return obj.photo_set.count()

    count_photos.short_description = "photo count"

    def save_model(self, request, obj, form, change):
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print(obj)
        print("change: ", change)
        super().save_model(request, obj, form, change)
