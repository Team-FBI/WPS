from rest_framework import serializers
from django.utils.text import slugify
from rooms import models as Room


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room.Room
        fields = ["id", "host", "title", "address", "image", "price", "description"]


class RoomCreateSerializer(serializers.ModelSerializer):
    capacity = serializers.ChoiceField(choices=Room.NO_OF_BEDS)
    room_type = serializers.ChoiceField(choices=Room.ROOM_TYPES)
    space = serializers.ChoiceField(choices=Room.SPACE_TYPES)
    bedroom = serializers.ChoiceField(choices=Room.NO_OF_ROOMS)
    bed_type = serializers.ChoiceField(choices=Room.BATHROOM_TYPES)
    bathroom = serializers.ChoiceField(choices=Room.NO_OF_ROOMS)
    cancellation = serializers.ChoiceField(choices=Room.CANCELATION_RULES)
    min_stay = serializers.ChoiceField(choices=Room.MIN_STAY)
    max_stay = serializers.ChoiceField(choices=Room.MAX_STAY)

    class Meta:
        model = Room.Room
        exclude = [
            "slug",
            "accuracy_rating",
            "location_rating",
            "communication_rating",
            "checkin_rating",
            "clean_rating",
            "value_rating",
            "total_rating",
            "id",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        title = validated_data.get("title")
        validated_data.update({"slug": slugify(title)})
        return super().create(validated_data)


class RoomDetailSerializer(serializers.ModelSerializer):
    capacity = serializers.ChoiceField(choices=Room.NO_OF_BEDS)
    room_type = serializers.ChoiceField(
        choices=Room.ROOM_TYPES, help_text=f"{Room.ROOM_TYPES}"
    )
    space = serializers.ChoiceField(
        choices=Room.SPACE_TYPES, help_text=f"{Room.SPACE_TYPES}"
    )
    bedroom = serializers.ChoiceField(choices=Room.NO_OF_ROOMS)
    bed_type = serializers.ChoiceField(
        choices=Room.BATHROOM_TYPES, help_text=f"{Room.BATHROOM_TYPES}"
    )
    bathroom = serializers.ChoiceField(choices=Room.NO_OF_ROOMS)
    cancellation = serializers.ChoiceField(
        choices=Room.CANCELATION_RULES, help_text=f"{Room.CANCELATION_RULES}"
    )
    min_stay = serializers.ChoiceField(choices=Room.MIN_STAY)
    max_stay = serializers.ChoiceField(choices=Room.MAX_STAY)

    class Meta:
        model = Room.Room
        fields = "__all__"


class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room.Reservation
        fields = ("price", "number_guest", "start_date", "end_date")

    def create(self, validated_data):
        validated_data["user"] = self.context.get("view").request.user
        room_id = self.context.get("view").request.room_id
        reservation = Room.Reservation.objects.create(**validated_data, room_id=room_id)
        return reservation
