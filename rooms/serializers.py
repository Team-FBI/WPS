from rest_framework import serializers
from django.utils.text import slugify
from rooms import models as Room


class RoomListSerializer(serializers.ModelSerializer):
    room_type = serializers.ChoiceField(
        source="get_room_type_display", choices=Room.ROOM_TYPES
    )
    space = serializers.ChoiceField(
        source="get_space_display", choices=Room.SPACE_TYPES
    )
    host = serializers.SerializerMethodField()
    bath_type = serializers.ChoiceField(
        source="get_beth_type_display", choices=Room.BATHROOM_TYPES
    )

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
        ]

    def get_host(self, obj):
        return obj.host.username


class RoomCreateSerializer(serializers.ModelSerializer):
    capacity = serializers.ChoiceField(choices=Room.NO_OF_BEDS)
    room_type = serializers.ChoiceField(
        choices=Room.ROOM_TYPES, help_text=f"{Room.ROOM_TYPES}"
    )
    space = serializers.ChoiceField(
        choices=Room.SPACE_TYPES, help_text=f"{Room.SPACE_TYPES}"
    )
    bedroom = serializers.ChoiceField(choices=Room.NO_OF_ROOMS)
    bath_type = serializers.ChoiceField(
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
        exclude = ["slug", "id", "total_rating", "created_at", "updated_at"]

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
    bath_type = serializers.ChoiceField(
        choices=Room.BATHROOM_TYPES, help_text=f"{Room.BATHROOM_TYPES}"
    )
    bathroom = serializers.ChoiceField(choices=Room.NO_OF_ROOMS)
    cancellation = serializers.ChoiceField(
        choices=Room.CANCELATION_RULES, help_text=f"{Room.CANCELATION_RULES}"
    )
    min_stay = serializers.ChoiceField(choices=Room.MIN_STAY)
    max_stay = serializers.ChoiceField(choices=Room.MAX_STAY)
    facilities = serializers.SerializerMethodField()
    reservations = serializers.SerializerMethodField()

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

    def get_facilities(self, obj):
        facilities = obj.facilities.all()
        return [v.name for v in facilities]

    def get_reservations(self, obj):
        reservations = obj.reservations.all()
        return [[v.start_date, v.end_date] for v in reservations]


class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room.Reservation
        exclude = ["id", "user", "room"]

    def create(self, validated_data):
        validated_data["user"] = self.context.get("view").request.user
        validated_data["room"] = Room.Room.objects.get(
            id=self.context.get("view").kwargs.get("pk")
        )
        return super().create(validated_data)


##### 토요일 추가
# from .models import RoomReview
# from django.db.models import Avg


# class RoomReviewListSerializer(serializers.ModelSerializer):
#     score_avg = RoomReview.objects.aggregate(
#         Avg("accuracy_score"),
#         Avg("location_score"),
#         Avg("communication_score"),
#         Avg("checkin_score"),
#         Avg("clean_score"),
#         Avg("value_score"),
#         Avg("total_score"),
#     )
#     accuracy_avg = serializers.FloatField(
#         data=round(score_avg("accuracy_score__avg"), 2)
#     )
#     location_avg = serializers.FloatField(
#         data=round(score_avg("location_score__avg"), 2)
#     )
#     communication_avg = serializers.FloatField(
#         data=round(score_avg("communication_score__avg"), 2)
#     )
#     checkin_avg = serializers.FloatField(data=round(score_avg("checkin_score__avg"), 2))
#     clean_avg = serializers.FloatField(data=round(score_avg("clean_score__avg"), 2))
#     value_avg = serializers.FloatField(data=round(score_avg("value_score__avg"), 2))
#     total_avg = serializers.FloatField(data=round(score_avg("total_score__avg"), 2))

#     class Meta:
#         model = RoomReview
#         fields = [
#             "user",
#             "description",
#             "created_at",
#             "accuracy_avg",
#             "location_avg",
#             "communication_avg",
#             "checkin_avg",
#             "clean_avg",
#             "value_avg",
#             "total_avg",
#         ]


# class RoomReviewCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RoomReview
#         fields = [
#             "description",
#             "accuracy_score",
#             "location_score",
#             "communication_score",
#             "checkin_score",
#             "clean_score",
#             "value_score",
#         ]


# class RoomReviewDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RoomReview
#         fields = [
#             "user",
#             "created_at",
#             "description",
#             "accuracy_score",
#             "location_score",
#             "communication_score",
#             "checkin_score",
#             "clean_score",
#             "value_score",
#         ]

