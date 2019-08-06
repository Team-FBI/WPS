from django.contrib import admin
from rooms.models import Room, Facility, RoomLike

# Register your models here.
class RoomOption(admin.ModelAdmin):
    list_display = ["id", "title", "slug", "state", "host"]
    list_display_links = ("title", "id", "slug")
    readonly_fields = [
        "slug",
        "total_rating",
        "accuracy_score",
        "location_score",
        "checkin_score",
        "clean_score",
        "communication_score",
        "value_score",
        "active",
    ]

class RoomLikeOption(admin.ModelAdmin):
    list_display = ["user", "room"]
    list_display_links = ("user", "room")

admin.site.register(RoomLike, RoomLikeOption)
admin.site.register(Room, RoomOption)
admin.site.register(Facility)
