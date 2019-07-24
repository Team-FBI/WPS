from rest_framework import serializers
from django.db.models import Q
from django.utils.text import slugify
from rooms import models as Room


class RoomListSerializer(serializers.ModelSerializer):
    host = serializers.SerializerMethodField()
    room_type = serializers.ChoiceField(
        source="get_room_type_display", choices=Room.ROOM_TYPES
    )
    space = serializers.ChoiceField(
        source="get_space_display", choices=Room.SPACE_TYPES
    )
    bath_type = serializers.ChoiceField(
        source="get_bath_type_display", choices=Room.BATHROOM_TYPES
    )
    room_type = serializers.ChoiceField(
        source="get_room_type_display", choices=Room.ROOM_TYPES
    )

    def get_host(self, obj):
        return obj.host.username

    class Meta:
        model = Room.Room
        fields = [
            "id",
            "host",
            "title",
            "image",
            "price",
            "description",
            "room_type",
            "space",
            "total_rating",
            "bedroom",
            "capacity",
            "bath_type",
            "address",
        ]


class RoomCreateSerializer(serializers.ModelSerializer):
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
        exclude = ["slug", "id", "created_at", "total_rating", "updated_at"]

    def create(self, validated_data):
        title = validated_data.get("title")
        validated_data.update({"slug": slugify(title, allow_unicode=True)})
        return super().create(validated_data)


class FacilityField(serializers.ModelSerializer):
    class Meta:
        model = Room.Facility
        fields = ["name"]


class RoomDetailSerializer(serializers.ModelSerializer):
    host = serializers.SerializerMethodField()
    capacity = serializers.ChoiceField(
        source="get_capacity_display", choices=Room.NO_OF_BEDS
    )
    room_type = serializers.ChoiceField(
        source="get_room_type_display", choices=Room.ROOM_TYPES
    )
    space = serializers.ChoiceField(
        source="get_space_display", choices=Room.SPACE_TYPES
    )
    bedroom = serializers.ChoiceField(
        source="get_bedroom_display", choices=Room.NO_OF_ROOMS
    )
    bath_type = serializers.ChoiceField(
        source="get_bath_type_display", choices=Room.BATHROOM_TYPES
    )
    bathroom = serializers.ChoiceField(
        source="get_bathroom_display", choices=Room.NO_OF_ROOMS
    )
    cancellation = serializers.ChoiceField(
        source="get_cancellation_display", choices=Room.CANCELATION_RULES
    )
    min_stay = serializers.ChoiceField(
        source="get_min_stay_display", choices=Room.MIN_STAY
    )
    max_stay = serializers.ChoiceField(
        source="get_max_stay_display", choices=Room.MAX_STAY
    )
    facilities = serializers.SerializerMethodField()
    reservations = serializers.SerializerMethodField()

    def get_facilities(self, obj):
        facilities = obj.facilities.all()
        return [v.name for v in facilities]

    def get_reservations(self, obj):
        reservations = obj.reservations.all()
        return [[v.start_date, v.end_date] for v in reservations if v.is_active]

    def get_host(self, obj):
        return obj.host.username

    class Meta:
        model = Room.Room
        fields = [
            "id",
            "title",
            "host",
            "address",
            "state",
            "postal_code",
            "mobile",
            "image",
            "image_1",
            "image_2",
            "image_3",
            "image_4",
            "total_rating",
            "capacity",
            "space",
            "room_type",
            "bedroom",
            "bath_type",
            "bathroom",
            "cancellation",
            "min_stay",
            "max_stay",
            "description",
            "price",
            "facilities",
            "reservations",
            "updated_at",
            "created_at",
        ]
