from django.db import models
from django.contrib.auth import get_user_model
from rooms.models import Room
from datetime import datetime


class RoomReservation(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="reservations"
    )
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="reservations"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(null=True, blank=False)
    accuracy_score = models.PositiveSmallIntegerField()
    location_score = models.PositiveSmallIntegerField()
    communication_score = models.PositiveSmallIntegerField()
    checkin_score = models.PositiveSmallIntegerField()
    clean_score = models.PositiveSmallIntegerField()
    value_score = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)
