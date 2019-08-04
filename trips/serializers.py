from rest_framework import serializers, pagination
from .models import *
from locations.models import State


class RecommendTrip(serializers.HyperlinkedModelSerializer):
    """
    메인 카테고리 페이지내에서 보여 줄 트립의 목록
    표시사항: 이름, 사진, 평점(평점갯수)
    """

    class Meta:
        model = Trip
        fields = (
            "name",
            "image_1",
            "rating_score",
            "duration_time",

        )


class TripStateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = State
        fields = (
            "name",
            "url",
            "pk",
        )


class TripProvideSerializer(serializers.ModelSerializer):
    provide_set = serializers.SlugRelatedField(queryset=State.objects.all(), slug_field="name")

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
            "review_count",
            "detail_category",
            "duration_time",
            "provides",
            "url",

        )


class TripCategorySerializer(serializers.HyperlinkedModelSerializer):
    """
    메인 페이지의 카테고리 분류
    """

    class Meta:
        model = TripCategory
        fields = (
            "url",
            "name",
            "image",
            "description",

        )


class TripCategoryDetailSerializer(serializers.HyperlinkedModelSerializer):
    """
    메인 페이지의 카테고리 상세 뷰
    """

    trips = TripCategoryOnly(many=True)

    class Meta:
        model = TripCategory
        fields = (

            "name",
            "image",
            "description",
            "trips",

        )


class TripReviewSerializer(serializers.ModelSerializer):
    user_set = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TripReview
        fields = (
            "user_set",
            "trip_set",
            "reservation_set",
            "description",
            "rating_score",
            "created_at",
        )


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


class TripListSerializer(serializers.HyperlinkedModelSerializer):
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


class TripReservationDetail(serializers.ModelSerializer):
    user_set = serializers.PrimaryKeyRelatedField(

        read_only=True,
    )

    class Meta:
        model = Reservation
        fields = "__all__"


from django.core.paginator import Paginator


class TripSerializer(serializers.HyperlinkedModelSerializer):
    host = serializers.ReadOnlyField(source='host.username')
    sub_category = serializers.SlugRelatedField(queryset=SubTripCategory.objects.all(), slug_field="name")
    compatibility = serializers.ChoiceField(source="get_compatibility_display", choices=COMPATIBILITY)
    technic = serializers.ChoiceField(source="get_technic_display", choices=BEGINNER)
    strength = serializers.ChoiceField(source="get_strength_display", choices=LIGHT)
    trip_reviews = serializers.SerializerMethodField('paginated_review')
    # trip_reviews = TripReviewDetailOnlySerializer(many=True)
    schedules = TripScheduleSerializer(many=True, source="trip_active")
    provides = TripProvideSerializer(many=True)
    state = serializers.SlugRelatedField(queryset=State.objects.all(), slug_field="name")

    def paginated_review(self, obj):
        page_size = self.context['request'].query_params.get('size') or 5
        paginator = Paginator(obj.trip_reviews.all(), page_size)
        page = self.context['request'].query_params.get('page') or 1
        print(paginator.page_range)

        words_in_book = paginator.page(page)
        serializer = TripReviewDetailOnlySerializer(words_in_book, many=True,
                                                    context={'request': self.context['request']})
        return serializer.data

    class Meta:
        model = Trip
        fields = (
            "pk",
            "name",
            "sub_category",
            "detail_category",
            "state",
            "duration_time",
            "provides",
            "schedules",
            "trip_reviews",
            "host",
            "host_about",
            "program",
            "additional_condition",
            "guest_material",
            "address",
            "place_info",
            "min_age",
            "max_guest",
            "certification",
            "price",
            "rating_score",
            "compatibility",
            "strength",
            "technic",
            "image_1",
            "image_2",
            "image_3",
            "image_4",
            "image_5",
            "image_6",
            "image_7",

        )


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
    user_set = serializers.PrimaryKeyRelatedField(

        read_only=True,
    )

    class Meta:
        model = Reservation
        fields = "__all__"
