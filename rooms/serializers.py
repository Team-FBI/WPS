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
    images = serializers.SerializerMethodField()
    reservations = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    def get_host(self, obj):
        return obj.host.username

    def get_images(self, obj):
        images = [obj.image, obj.image_1, obj.image_2, obj.image_3, obj.image_4]
        result = [1 for img in images if img]
        return len(result)

    def get_reservations(self, obj):
        return obj.reservations.count()

    def get_state(self, obj):
        return obj.state.name

    def get_label(self, obj):
        result = None
        if int(obj.total_rating) > 4:
            result = "plus"
        if obj.host.is_staff:
            result = "luxe"
        return result

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
            "images",
            "reservations",
            "state",
            "label",
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
    images = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    def get_facilities(self, obj):
        facilities = obj.facilities.all()
        return [v.name for v in facilities]

    def get_reservations(self, obj):
        reservations = obj.reservations.all()
        return [[v.start_date, v.end_date] for v in reservations if v.is_active]

    def get_host(self, obj):
        return obj.host.username
    
    def get_state(self, obj):
        return obj.state.name

    def get_images(self, obj):
        images = [obj.image, obj.image_1, obj.image_2, obj.image_3, obj.image_4]
        result = [1 for img in images if img]
        return len(result)

    def get_label(self, obj):
        result = None
        if int(obj.total_rating) > 4:
            result = "plus"
        if obj.host.is_staff:
            result = "luxe"
        return result

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
            "images",
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
            "label",
        ]
