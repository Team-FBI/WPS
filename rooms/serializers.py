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
    reservations = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    super_host = serializers.SerializerMethodField()
    facilities = serializers.SerializerMethodField()

    def get_facilities(self, obj):
        facilities = obj.facilities.all()
        return [v.name for v in facilities]

    def get_host(self, obj):
        return obj.host.username

    def get_reservations(self, obj):
        return obj.reservations.count()

    def get_state(self, obj):
        return obj.state.name

    def get_label(self, obj):
        result = None
        if int(obj.total_rating) >= 4:
            result = "plus"
        if obj.host.is_staff:
            result = "luxe"
        return result

    def get_super_host(self, obj):
        if obj.host.rooms.filter(total_rating__gte=3.8).count() > 3:
            return True

    def get_facilities(self, obj):
        facilities = obj.facilities.all()
        return [v.name for v in facilities]

    class Meta:
        model = Room.Room
        fields = [
            "id",
            "host",
            "title",
            "image",
            "image_1",
            "image_2",
            "image_3",
            "image_4",
            "price",
            "description",
            "room_type",
            "space",
            "total_rating",
            "bedroom",
            "beds",
            "bathroom",
            "capacity",
            "bath_type",
            "address",
            "reservations",
            "state",
            "label",
            "super_host",
            "facilities",
        ]


class RoomCreateSerializer(serializers.ModelSerializer):
    room_type = serializers.ChoiceField(
        choices=Room.ROOM_TYPES, help_text=f"{Room.ROOM_TYPES}"
    )
    space = serializers.ChoiceField(
        choices=Room.SPACE_TYPES, help_text=f"{Room.SPACE_TYPES}"
    )
    bed_type = serializers.ChoiceField(
        choices=Room.BATHROOM_TYPES, help_text=f"{Room.BATHROOM_TYPES}"
    )
    cancellation = serializers.ChoiceField(
        choices=Room.CANCELATION_RULES, help_text=f"{Room.CANCELATION_RULES}"
    )

    class Meta:
        model = Room.Room
        exclude = [
            "slug",
            "id",
            "created_at",
            "updated_at",
            "total_rating",
            "clean_score",
            "accuracy_score",
            "value_score",
            "location_score",
            "communication_score",
            "checkin_score",
        ]


class FacilityField(serializers.ModelSerializer):
    class Meta:
        model = Room.Facility
        fields = ["name"]


class RoomDetailSerializer(serializers.ModelSerializer):
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
    cancellation = serializers.ChoiceField(
        source="get_cancellation_display", choices=Room.CANCELATION_RULES
    )
    facilities = serializers.SerializerMethodField()
    reservations = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    super_host = serializers.SerializerMethodField()

    def get_facilities(self, obj):
        facilities = obj.facilities.all()
        return [v.name for v in facilities]

    def get_reservations(self, obj):
        reservations = obj.reservations.all()
        return [[v.start_date, v.end_date] for v in reservations if v.is_active]

    def get_host(self, obj):
        email = obj.host.email or None
        img = obj.host.image.url or None
        return [obj.host.username, email, img]

    def get_state(self, obj):
        return obj.state.name

    def get_label(self, obj):
        result = None
        if int(obj.total_rating) >= 4:
            result = "plus"
        if obj.host.is_staff:
            result = "luxe"
        return result

    def get_super_host(self, obj):
        if obj.host.rooms.filter(total_rating__gte=3.8).count() > 3:
            return True

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
            "image_5",
            "image_6",
            "total_rating",
            "capacity",
            "space",
            "room_type",
            "bedroom",
            "beds",
            "bath_type",
            "bathroom",
            "cancellation",
            "min_stay",
            "max_stay",
            "description",
            "locational_description",
            "price",
            "facilities",
            "reservations",
            "updated_at",
            "created_at",
            "label",
            "accuracy_score",
            "location_score",
            "communication_score",
            "checkin_score",
            "clean_score",
            "value_score",
            "super_host",
        ]
