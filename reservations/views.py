from datetime import datetime, timedelta

from django.db.models import Q, Avg
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from config.utils import response_error_handler

from reservations.models import RoomReservation
from rooms.models import Room

from reservations.serializers import (
    ReservationUpdateSerializer,
    ReservationCreateSerializer,
    ReservationDetailSerializer,
)


def reservation_validation(queryset, start_date, end_date):
    if start_date and end_date:
        try:
            # date reservatable validation
            start_time = datetime(
                *[v for v in map(lambda el: int(el), start_date.split("-"))]
            )
            end_time = datetime(
                *[v for v in map(lambda el: int(el), end_date.split("-"))]
            )
        except Exception:
            raise ValueError(
                "date format you passed, is not right format", "type in year-month-day"
            )
        if start_time > end_time:
            raise ValueError(
                "start day could not be later than end date",
                "retype form data"
            )
        condition_date_1_1 = Q(reservations__start_date__lte=start_time)
        condition_date_1_2 = Q(reservations__end_date__gte=start_time)
        condition_date_2_1 = Q(reservations__start_date__lte=end_time)
        condition_date_2_2 = Q(reservations__end_date__gte=end_time)
        queryset = queryset.filter(
            ~(condition_date_1_1 & condition_date_1_2)
        ).filter(~(condition_date_2_1 & condition_date_2_2))
        if not queryset:
            return queryset

        # stayable day validation
        stay = end_time - start_time
        min_stay = int(queryset[0].min_stay)
        max_stay = int(queryset[0].max_stay)
        print(min_stay, max_stay)
        if not (stay >= timedelta(min_stay) and stay <= timedelta(max_stay)):
            raise ValueError(
                "your trying to stay is not match to room's condition",
                "look at stayable days of room.",
                )
        print("passed")
    return queryset


class ReservationDetailUpdateView(generics.RetrieveUpdateAPIView):
    """A function, able to get, update detail of reservation.
    
    Arguments:
        generics {[RetrieveUpdateAPIView]} -- [GET, PUT hanlder]
    
    Raises:
        PermissionError: [GET-HTTP_401_UNAUTHORIZED]
        PermissionError: [PUT-HTTP_401_UNAUTHORIZED]
        ValueError: [PUT-HTTP_404_NOT_FOUND]    
    
    Returns:
        [status] -- [GET-HTTP_200_OK]
        [status] -- [PUT-HTTP_202_ACCEPTED]
    """

    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        serializer_class = ReservationDetailSerializer
        if self.request.method == "PUT":
            serializer_class = ReservationUpdateSerializer
        return serializer_class

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        queryset = RoomReservation.objects.filter(id=pk)
        if not queryset:
            raise ValueError("Reservation not exist", "check out your reservation id")
        return queryset

    @response_error_handler
    def get(self, request, *args, **kwargs):
        if (
            request.user == self.get_queryset()[0].user
            or request.user == self.get_queryset()[0].room.host
        ):
            return super().get(request, *args, **kwargs)
        raise PermissionError(
            "only owner of reservation or host of room could do this", "dont do it"
        )

    @response_error_handler
    def put(self, request, *args, **kwargs):
        if not (request.user == self.get_queryset()[0].user):
            raise PermissionError(
                "only Owner of reservation could do this", "dont do it"
            )
        if self.get_queryset()[0].start_date >= datetime.now():
            raise ValueError(
                "start date not passed", "evaluate your reservation after first-day"
            )
        super().put(request, *args, **kwargs)
        room_id = int(self.get_queryset()[0].room_id)
        reservations = RoomReservation.objects.filter(room=room_id).aggregate(
            Avg("accuracy_score"),
            Avg("location_score"),
            Avg("communication_score"),
            Avg("checkin_score"),
            Avg("clean_score"),
            Avg("value_score"),
        )
        total = 0
        for key, val in reservations.items():
            total += val
        total = round(total / 7, 2)
        Room.objects.filter(id=room_id).update(total_rating=total)
        return Response(data=None, status=status.HTTP_202_ACCEPTED)


class ReservationCreateView(generics.CreateAPIView):
    """A function, able to POST Reservation create request.
    
    Arguments:
        generics {[CreateAPIView]} -- [POST handler]
    
    Raises:
        ValueError: [POST-HTTP_404_NOT_FOUND]
        ValidationError: [POST-HTTP_400_BAD_REQUEST]
    
    Returns:
        [status] -- [POST-HTTP_201_CREATED]
    """

    serializer_class = ReservationCreateSerializer
    permission_classes = (IsAuthenticated,)
    queryset = RoomReservation.objects.all()

    @response_error_handler
    def post(self, request, *args, **kwargs):
        start_date, end_date = request.data["start_date"], request.data["end_date"]
        room = Room.objects.filter(id=self.kwargs.get("pk"))

        if reservation_validation(room, start_date, end_date):
            return super().post(request, *args, **kwargs)
        raise ValueError("Date already reservated!", "check for another date.")

