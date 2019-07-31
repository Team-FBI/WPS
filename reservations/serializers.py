from rest_framework import serializers
from reservations.models import RoomReservation


class ReservationDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = RoomReservation
        fields = "__all__"

    def get_user(self, obj):
        return obj.user.username


class ReservationCreateSerializer(serializers.ModelSerializer):
    message = serializers.CharField(write_only=True)

    class Meta:
        model = RoomReservation
        fields = ["start_date", "end_date", "message"]

    def create(self, validated_data):
        message = validated_data.pop('message')
        reservation = super().create(validated_data)
        reservation.messages.create(
            author=reservation.user,
            text=message,
        )
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
