from rest_framework import serializers
from reservations.models import RoomReservation
from rooms.models import Room

class ReservationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomReservation
        fields = "__all__"


class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomReservation
        fields = ["start_date", "end_date"]

    def create(self, validated_data):
        validated_data["user"] = self.context.get("view").request.user
        validated_data["room"] = Room.objects.get(
            id=self.context.get("view").kwargs.get("pk")
        )
        print(validated_data)
        return super().create(validated_data)


class ReservationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomReservation
        exclude = ["start_date", "end_date", "id", "room", "user"]

