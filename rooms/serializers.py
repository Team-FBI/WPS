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



##### 토요일 추가
from .models import RoomReview
from django.db.models import Avg

class RoomReviewListSerializer(serializers.ModelSerializer):
    score_avg = RoomReview.objects.aggregate(Avg('accuracy_score'), Avg('location_score'), Avg('communication_score'),
                                             Avg('checkin_score'), Avg('clean_score'), Avg('value_score'),
                                             Avg('total_score'))
    accuracy_avg = serializers.FloatField(data=round(score_avg("accuracy_score__avg"), 2))
    location_avg = serializers.FloatField(data=round(score_avg("location_score__avg"), 2))
    communication_avg = serializers.FloatField(data=round(score_avg("communication_score__avg"), 2))
    checkin_avg = serializers.FloatField(data=round(score_avg("checkin_score__avg"), 2))
    clean_avg = serializers.FloatField(data=round(score_avg("clean_score__avg"), 2))
    value_avg = serializers.FloatField(data=round(score_avg("value_score__avg"), 2))
    total_avg = serializers.FloatField(data=round(score_avg("total_score__avg"), 2))

    class Meta:
        model = RoomReview
        fields = [
            "user", "description", "created_at", "accuracy_avg", "location_avg", "communication_avg",
            "checkin_avg", "clean_avg", "value_avg", "total_avg"
        ]


class RoomReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomReview
        fields = ['description', 'accuracy_score', 'location_score', 'communication_score', 'checkin_score',
                  'clean_score', 'value_score']


class RoomReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomReview
        fields = ['user', "created_at", 'description', 'accuracy_score', 'location_score',
                  'communication_score', 'checkin_score', 'clean_score', 'value_score'
                  ]