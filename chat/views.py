from django.shortcuts import render
from django.utils.safestring import mark_safe
from rest_framework import generics
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
import json
from reservations.models import RoomReservation
from .serializers import ReservationSerializer, ReservationListSerializer, MessageSerializer
from .models import Message


# TODO: remove when tests ends
def view_room(request, reservation_id):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(reservation_id))
    })


class MessageCreateView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ReservationViewSet(ReadOnlyModelViewSet):
    queryset = RoomReservation.objects.all()
    serializer_class = ReservationSerializer

    def list(self, request, *args, **kwargs):
        user_id = self.request.user.id
        self.queryset = RoomReservation.objects.filter(user_id=user_id)
        self.serializer_class = ReservationListSerializer
        return super().list(request, *args, **kwargs)
