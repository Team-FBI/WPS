from rest_framework import serializers
from reservations.models import RoomReservation
from rooms.models import Room
from chat.models import Message


class ReservationDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = RoomReservation
        fields = "__all__"

    def get_user(self, obj):
        return obj.user.username


class ReservationCreateSerializer(serializers.ModelSerializer):
    messages = serializers.CharField(write_only=True)

    class Meta:
        model = RoomReservation
        fields = ["start_date", "end_date", "messages"]

    def create(self, validated_data):
        validated_data["user"] = self.context.get("view").request.user
        validated_data["room"] = Room.objects.get(
            id=self.context.get("view").kwargs.get("pk")
        )
        text = validated_data.pop("messages")
        reservation = super().create(validated_data)
        Message.objects.create(author=validated_data["user"], reservation=reservation,
                               text=text)
        return reservation


class ReservationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomReservation
        exclude = ["start_date", "end_date", "id", "room", "user", "is_active"]

    def update(self, instance, validated_data):
        scores = [int(v) for v in validated_data.values() if isinstance(v, int)]
        if not (len(scores) is 6):
            raise ValueError("all 6 score should be sepecified in integer", "and no digits!")
        for score in scores:
            if score > 5 or score < 0:
                raise ValueError("score should be in 0~5 in integer", "and no digits!")
        instance.is_active = False
        instance.save()
        return super().update(instance, validated_data)
