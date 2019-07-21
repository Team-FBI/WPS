from django.contrib import admin
from rooms.models import Room, Reservation, Facility

# Register your models here.

admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Facility)
