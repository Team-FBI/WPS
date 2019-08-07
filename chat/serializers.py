from django.contrib.auth import get_user_model
from rest_framework import serializers
from rooms.models import Room
from reservations.models import RoomReservation
from .models import Message

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'image')


class RoomSerializer(serializers.ModelSerializer):
    host = UserSerializer()

    class Meta:
        model = Room
        fields = ('id', 'title', 'price', 'host')


class MessageSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    is_host = serializers.BooleanField(read_only=True)
    created = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", read_only=True)

    class Meta:
        model = Message
        fields = ('author', 'is_host', 'text', 'created')

    def create(self, validated_data):
        view_context = self.context.get("view")
        validated_data["author"] = view_context.request.user
        validated_data["reservation_id"] = view_context.kwargs.get("pk")
        return super().create(validated_data)


class ReservationSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    user = UserSerializer()
    messages = MessageSerializer(many=True)

    class Meta:
        model = RoomReservation
        fields = ('id', 'user', 'start_date', 'end_date', 'room', 'messages')


class ReservationListSerializer(ReservationSerializer):
    messages = serializers.SerializerMethodField(method_name='get_latest_message')

    def get_latest_message(self, obj):
        return MessageSerializer(obj.messages.latest('created')).data
