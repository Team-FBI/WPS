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

    def get_queryset(self):
        user = self.request.user
        user_type = self.request.query_params.get('user_type')
        queryset = RoomReservation.objects.filter(user=user)

        if user_type == 'host':
            queryset = RoomReservation.objects.filter(room__host=user)
        return queryset

    def list(self, request, *args, **kwargs):
        self.serializer_class = ReservationListSerializer
        return super().list(request, *args, **kwargs)
