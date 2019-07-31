from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Provide)
admin.site.register(TripProvide)
admin.site.register(Trip)
admin.site.register(TripSchedule)
admin.site.register(TripCategory)
admin.site.register(SubTripCategory)
admin.site.register(Reservation)
admin.site.register(TripReview)