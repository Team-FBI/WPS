from rest_framework import serializers
from rooms import models as Room
from .models import Booking, ReservedDates

class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room.Room
        fields = [
            "id",
            "host",
            "title",
            "address",
            "image",
            "price",
            "description",
        ]

class RoomCreateSerializer(serializers.ModelSerializer):
    capacity = serializers.ChoiceField(
        source="get_capacity_display", choices=Room.NO_OF_BEDS
    )
    room_type = serializers.ChoiceField(
        source="get_room_type_display", choices=Room.PLACE_TYPES
    )
    space = serializers.ChoiceField(
        source="get_space_display", choices=Room.SPACE_TYPES
    )
    bedroom = serializers.ChoiceField(
        source="get_bedroom_display", choices=Room.NO_OF_ROOMS
    )
    bed_type = serializers.ChoiceField(
        source="get_bed_type_display", choices=Room.BATHROOM_TYPES
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
    class Meta:
        model = Room.Room
        # fields = [
        #     "title",
        #     "address",
        #     "state",
        #     "postal_code",
        #     "mobile",
        #     "image",
        #     "price",
        #     "description",
        #     "files",
        #     "active",
        #     ""
        # ]
        exclude = [
            "slug",
            "accuracy_rating",
            "location_rating",
            "communication_rating",
            "checkin_rating",
            "clean_rating",
            "value_rating",
            "id",
            "created_at",
            "updated_at",
            "host",
        ]

class RoomDetailSerializer(serializers.ModelSerializer):
    capacity = serializers.ChoiceField(
        source="get_capacity_display", choices=Room.NO_OF_BEDS
    )
    room_type = serializers.ChoiceField(
        source="get_room_type_display", choices=Room.PLACE_TYPES
    )
    space = serializers.ChoiceField(
        source="get_space_display", choices=Room.SPACE_TYPES
    )
    bedroom = serializers.ChoiceField(
        source="get_bedroom_display", choices=Room.NO_OF_ROOMS
    )
    bed_type = serializers.ChoiceField(
        source="get_bed_type_display", choices=Room.BATHROOM_TYPES
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
    accuracy_rating = serializers.ChoiceField(
        source="get_accuracy_rating_display", choices=Room.PLACE_RATING
    )
    location_rating = serializers.ChoiceField(
        source="get_location_rating_display", choices=Room.PLACE_RATING
    )
    communication_rating = serializers.ChoiceField(
        source="get_communication_rating_display", choices=Room.PLACE_RATING
    )
    checkin_rating = serializers.ChoiceField(
        source="get_checkin_rating_display", choices=Room.PLACE_RATING
    )
    clean_rating = serializers.ChoiceField(
        source="get_clean_rating_display", choices=Room.PLACE_RATING
    )
    value_rating = serializers.ChoiceField(
        source="get_value_rating_display", choices=Room.PLACE_RATING
    )
    class Meta:
        model = Room.Room
        fields = "__all__"

class BookingCreateSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "user",
            "reservation",
            "room",
            "price",
            "number_guest",
            "nights",
            "start_date",
            "end_date",
        )

    def create(self, validated_data):
        validated_data
        ReservedDates.create