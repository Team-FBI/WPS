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
    accuracy_score = models.PositiveSmallIntegerField(default=0)
    location_score = models.PositiveSmallIntegerField(default=0)
    communication_score = models.PositiveSmallIntegerField(default=0)
    checkin_score = models.PositiveSmallIntegerField(default=0)
    clean_score = models.PositiveSmallIntegerField(default=0)
    value_score = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    # def __contains__(self, somedate):
    #     start, end = somedate
    #     #스타트 가 스타트와 엔드 사이에 있다
    #     condition_a_1 = start >= self.start_date
    #     condition_a_2 = start < self.end_date
    #     condition_b_1 = end > self.start_date
    #     condition_b_2 = end <= self.end_date
    #     return (condition_a_1 and condition_a_2) or (condition_b_1 and condition_b_2)
