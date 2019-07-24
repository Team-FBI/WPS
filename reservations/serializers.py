from rest_framework import serializers
from reservations.models import RoomReservation
from rooms.models import Room

class ReservationDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = RoomReservation
        exclude = ("start_date", "end_date")

    def get_user(self, obj):
        return obj.user.username


class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomReservation
        fields = ["start_date", "end_date"]

    def create(self, validated_data):
        validated_data["user"] = self.context.get("view").request.user
        validated_data["room"] = Room.objects.get(
            id=self.context.get("view").kwargs.get("pk")
        )
        return super().create(validated_data)


class ReservationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomReservation
        exclude = ["start_date", "end_date", "id", "room", "user", "is_active"]

    def update(self, instance, validated_data):
        instance.is_active=False
        instance.save()
        return super().update(instance, validated_data)


