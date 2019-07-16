from django.contrib import admin
from rooms.models import Room, ReservedDates, Booking

# Register your models here.

admin.site.register(Room)
admin.site.register(ReservedDates)
admin.site.register(Booking)
