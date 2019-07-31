from rest_framework import serializers
from .models import *
from locations.models import State


class RecommendTrip(serializers.HyperlinkedModelSerializer):
    """
    메인 카테고리 페이지내에서 보여 줄 트립의 목록
    표시사항: 이름, 사진, 평점(평점갯수)
    """

    # provides = serializers.StringRelatedField(many=True)

    class Meta:
        model = Trip
        fields = (
            "name",
            "image_1",
            "rating_score",
            "duration_time",
            # "provides",
            # "url",

        )


class TripStateSerializer(serializers.HyperlinkedModelSerializer):
    trips = RecommendTrip(read_only=True)

    class Meta:
        model = State
        fields = (
            "url",
            "name",
            "trips",
        )


class TripProvideSerializer(serializers.ModelSerializer):

    class Meta:
        model = TripProvide
        fields = (
            "provide_set",
            "description",
        )


class TripCategoryOnly(serializers.HyperlinkedModelSerializer):
    """
    메인 카테고리 페이지내에서 보여 줄 트립의 목록
    """
    provides = serializers.StringRelatedField(many=True)

    class Meta:
        model = Trip
        fields = (
            "name",
            "image_1",
            "rating_score",
            "duration_time",
            "provides",
            "url",

        )


class TripCategorySerializer(serializers.HyperlinkedModelSerializer):
    trips = TripCategoryOnly(many=True)

    class Meta:
        model = TripCategory
        fields = (
            "url",
            "pk",
            "name",
            "description",
            "trips",

        )


class TripReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripReview
        fields = (
            "__all__"
        )

    def create(self, validated_data):
        validated_data["user_set"] = self.context.get("view").request.user
        return super().create(validated_data)


class TripReviewDetailOnlySerializer(serializers.ModelSerializer):
    user_set = serializers.ReadOnlyField(source='user_set.username')

    class Meta:
        model = TripReview
        fields = (
            "user_set",
            "description",
            "rating_score",
            "created_at",
        )

    def create(self, validated_data):
        validated_data["user_set"] = self.context.get("view").request.user
        return super().create(validated_data)


class TripScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripSchedule
        fields = (
            "id",
            "start_datetime",
            "end_datetime",
            "capacity",
            "now_guest_count",
            "active",
        )


class TripSerializer(serializers.HyperlinkedModelSerializer):
    host = serializers.ReadOnlyField(source='host.username')
    trip_category = serializers.SlugRelatedField(queryset=TripCategory.objects.all(), slug_field="name")
    compatibility = serializers.ChoiceField(source="get_compatibility_display", choices=COMPATIBILITY)
    technic = serializers.ChoiceField(source="get_technic_display", choices=BEGINNER)
    strength = serializers.ChoiceField(source="get_strength_display", choices=LIGHT)
    trip_reviews = TripReviewDetailOnlySerializer(many=True)
    schedules = TripScheduleSerializer(many=True, source="trip_active")
    provides = TripProvideSerializer(many=True)

    class Meta:
        model = Trip
        fields = (
            "__all__"
        )

    # def create(self, validated_data):
    #     review_data = validated_data.pop('trip_reviews')
    #     review_data["user_set"] = self.context.get("view").request.user
    #     trip_id = Trip.objects.get(id=self.context.get("view").kwargs.get("pk"))
    #     user_id = self.context.get("view").request.user
    #     user = User.objects.get(pk=user_id)
    #     user_reservation = user.reservation.all().filter(trip_schedule__trip_set=trip_id)
    #
    #     review_data["reservation"] = user_reservation
    #     Profile.objects.create(user=user, **profile_data)
    #     return user


class SubCategorySerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=TripCategory.objects.all(), slug_field="name")
    state = serializers.SlugRelatedField(queryset=TripCategory.objects.all(), slug_field="name")

    class Meta:
        model = SubTripCategory
        fields = "__all__"


class RecommendTripSerializer(serializers.ModelSerializer):
    provides = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = (
            "name",
            "image_1",
            "rating_score",
            "duration_time",
            "provides",
            "url",
        )


class TestSerializer(serializers.HyperlinkedModelSerializer):
    trips = TripCategoryOnly(many=True, read_only=True)

    class Meta:
        model = State
        fields = (

            "name",
            "trips",

        )


class TripReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"

    def create(self, validated_data):
        validated_data["user_set"] = self.context.get("view").request.user
        return super().create(validated_data)
