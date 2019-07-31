from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.shortcuts import get_object_or_404
import random


class StateList(generics.ListCreateAPIView):
    queryset = State.objects.all()
    serializer_class = TripStateSerializer
    name = "state-list"


class StateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = State.objects.all()
    serializer_class = TestSerializer
    sub_category_queryset = SubTripCategory.objects.all()
    sub_category_serializer_class = SubCategorySerializer
    trip_queryset = Trip.objects.all()
    trip_serializer_class = TripCategoryOnly
    name = 'state-detail'

    # 지역별 랜덤 트립 추천을 위한 것
    def get_trip_queryset(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        # return Trip.objects.all().filter(state_id=filter_kwargs["pk"])[:13]
        trip_queryset = Trip.objects.all().filter(state_id=filter_kwargs["pk"])
        max_id = trip_queryset.count()
        # random_queryset = Trip.objects.none()
        while True:
            random_index = random.randint(0, max_id)
            random_queryset = trip_queryset[random_index:random_index + 1]
            if random_queryset.count() == 1:
                break
        return random_queryset

    def get_best_trip_queryset(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        return Trip.objects.all().filter(state_id=filter_kwargs["pk"])[:6]

    def get_trip_serializer(self, *args, **kwargs):
        trip_serializer_class = self.get_trip_serializer_class()
        kwargs['context'] = self.get_trip_serializer_context()
        return trip_serializer_class(*args, **kwargs)

    def get_trip_serializer_class(self):
        assert self.sub_category_serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        return self.trip_serializer_class

    def get_trip_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    # 지역별 카테고리 표시를 위한 것
    def get_sub_category_queryset(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        return SubTripCategory.objects.all().filter(state_id=filter_kwargs["pk"])

    def get_sub_category_serializer_class(self):
        assert self.sub_category_serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        return self.sub_category_serializer_class

    def get_sub_category_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_sub_category_serializer(self, *args, **kwargs):
        sub_category_serializer_class = self.get_sub_category_serializer_class()
        kwargs['context'] = self.get_sub_category_serializer_context()
        return sub_category_serializer_class(*args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance2 = self.filter_queryset(self.get_sub_category_queryset())
        instance3 = self.filter_queryset(self.get_trip_queryset())
        instance4 = self.filter_queryset(self.get_best_trip_queryset())
        serializer = self.get_serializer(instance)
        serializer2 = self.get_sub_category_serializer(instance2, many=True)
        serializer3 = self.get_trip_serializer(instance3, many=True)
        serializer4 = self.get_trip_serializer(instance4, many=True)
        context = {
            "state_detail": serializer.data,
            "sub_trip_category": serializer2.data,
            "random_recommend_trip12": serializer3.data,
            "best_trip": serializer4.data,
        }
        return Response(context)


class TripCategoryList(generics.ListCreateAPIView):
    queryset = TripCategory.objects.all()
    serializer_class = TripCategorySerializer
    state_queryset = State.objects.all()
    state_serializer_class = TripStateSerializer
    name = 'tripcategory-list'

    def get_state_queryset(self):
        return State.objects.all()

    def get_state_serializer_class(self):
        assert self.state_serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        return self.state_serializer_class

    def get_state_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_state_serializer(self, *args, **kwargs):
        state_serializer_class = self.get_state_serializer_class()
        kwargs['context'] = self.get_state_serializer_context()
        return state_serializer_class(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        queryset = self.filter_queryset(self.get_state_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_state_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_state_serializer(queryset, many=True)
        context = {
            "categories": response.data,
            "state": serializer.data,

        }
        return Response(context)


class TripCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TripCategory.objects.all()
    serializer_class = TripCategorySerializer
    state_queryset = State.objects.all()
    state_serializer_class = TripStateSerializer
    name = 'tripcategory-detail'

    def get_state_queryset(self):
        return State.objects.all()

    def get_state_serializer_class(self):
        assert self.state_serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        return self.state_serializer_class

    def get_state_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_state_serializer(self, *args, **kwargs):
        state_serializer_class = self.get_state_serializer_class()
        kwargs['context'] = self.get_state_serializer_context()
        return state_serializer_class(*args, **kwargs)

    def get_state_object(self):
        queryset = self.filter_queryset(self.get_state_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance2 = self.get_state_object()
        serializer = self.get_serializer(instance)
        serializer2 = self.get_state_serializer(instance2)
        context = {
            "serializer": serializer.data,
            "serializer2": serializer2.data,
        }
        return Response(context)


class TripList(generics.ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    name = 'trip-list'


class TripDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    name = 'trip-detail'


class TripReservationCreate(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = TripReservationCreateSerializer
    name = "trip-reservation-create"

    def reservation_checker(self, guest_count, trip_schedule):
        guest_capacity = TripSchedule.objects.get(pk=trip_schedule).capacity
        guest_now = TripSchedule.objects.get(pk=trip_schedule).now_guest_count
        guest_check = guest_capacity - guest_now
        if int(guest_count) <= guest_check:
            return True
        else:
            return False

    def schdule_checker(self, trip, trip_schedule):
        trip_object = Trip.objects.get(pk=int(trip))
        schedule_object = TripSchedule.objects.get(pk=int(trip_schedule))
        if schedule_object in trip_object.schedules.all():
            return True
        else:
            return False

    def post(self, request, *args, **kwargs):
        trip_schedule = request.data["trip_schedule"]
        guest_count = request.data["guest_count"]
        trip = request.data["trip_set"]
        # total_price_check = Trip.objects.get(pk=trip).price * int(guest_count)
        # total_price = request.data["total_price"]
        # print(request.data)
        if not self.schdule_checker(trip, trip_schedule):
            raise ValueError("잘못된 스케줄 입니다", "스케줄을 확인해주세요")
        if self.reservation_checker(guest_count, trip_schedule):
            return super().post(request, *args, **kwargs)
        raise ValueError("인원수가 맞지 않습니다", "인원수를 확인 해주세요")

    def perform_create(self, serializer):
        serializer.save()
        guest_count = serializer.data["guest_count"]
        trip_set = serializer.data["trip_schedule"]
        # 트립 스케줄의 인원수 업데이트
        schedule = TripSchedule.objects.get(pk=trip_set)
        schedule_now_guest_count = schedule.now_guest_count
        schedule.now_guest_count = schedule_now_guest_count + guest_count
        if schedule.capacity == schedule.now_guest_count:
            schedule.active = False
        schedule.save()


class TripReviewCreate(generics.ListCreateAPIView):
    queryset = TripReview.objects.all()
    serializer_class = TripReviewSerializer
    name = "trip-review"



    # def

    # def post(self, request, *args, **kwargs):
    #     # trip = request.data["trip_set"]
    #     # reservation = request.data["reservation_set"]
    #     return super().post(request, *args, **kwargs)

    # trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trip_reviews")
    # reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="trip_reviews")
    # description = models.TextField(blank=True)
    # rating_score = models.SmallIntegerField(default=5)


#
#
# class PlayerList(generics.ListCreateAPIView):
#     queryset = Player.objects.all()
#     serializer_class = PlayerSerializer
#     name = 'player-list'
#
#
# class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Player.objects.all()
#     serializer_class = PlayerSerializer
#     name = 'player-detail'
#
#
# class PlayerScoreList(generics.ListCreateAPIView):
#     queryset = PlayerScore.objects.all()
#     serializer_class = PlayerScoreSerializer
#     name = 'playerscore-list'
#
#
# class PlayerScoreDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = PlayerScore.objects.all()
#     serializer_class = PlayerScoreSerializer
#     name = 'playerscore-detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            # 'players': reverse(PlayerList.name, request=request),
            'trip-category': reverse(TripCategoryList.name, request=request),
            'trip': reverse(TripList.name, request=request),
            "trip/reservation": reverse(TripReservationCreate.name, request=request),
            "trip/state": reverse(StateList.name, request=request),
            "trip/review": reverse(TripReviewCreate.name, request=request)

        })
