from django.contrib import admin
from reservations.models import RoomReservation
# Register your models here.

class ReservationOption(admin.ModelAdmin):
    list_display = ["id", "room", "user", "start_date", "end_date"]
    list_display_links = ("id", "room", "user")
    readonly_fields = [
        "accuracy_score",
        "location_score",
        "checkin_score",
        "clean_score",
        "communication_score",
        "value_score",
        "is_active",
    ]

admin.site.register(RoomReservation, ReservationOption)