from django.db import models
from django.contrib.auth import get_user_model
from reservations.models import RoomReservation


class Message(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_host = models.BooleanField(default=False)
    reservation = models.ForeignKey(RoomReservation, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
