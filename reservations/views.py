from datetime import date, timedelta

from django.db.models import Q, Avg, QuerySet
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


def reservation_validation(queryset: QuerySet, start_date, end_date):
    if start_date and end_date:
        try:
            # date reservatable validation
            formatter = lambda el: int(el) if el[0] is not "0" else int(el[1:])
            start_time = date(*[v for v in map(formatter, start_date.split("-"))])
            end_time = date(*[v for v in map(formatter, end_date.split("-"))])
            if start_time == end_time:
                raise ValueError(
                    "start date and end date is same,", "at least 1 day plz"
                )

        except Exception:
            raise ValueError(
                "date format you passed, is not right format", "type in year-month-day"
            )
        if start_time > end_time:
            raise ValueError(
                "start day could not be later than end date", "retype form data"
            )
        # stayable day validation
        stay = end_time - start_time
        min_stay = Q(min_stay__lte=stay.days)
        max_stay = Q(max_stay__gte=stay.days)
        # stayable date validation
        condition_date_1_1 = Q(start_date__lte=start_time)
        condition_date_1_2 = Q(end_date__gt=start_time)
        condition_date_2_1 = Q(start_date__lt=end_time)
        condition_date_2_2 = Q(end_date__gte=end_time)
        condition_a = Q((condition_date_1_1 & condition_date_1_2))
        condition_b = Q((condition_date_2_1 & condition_date_2_2))
        condition_primary = Q(min_stay & max_stay)
        queryset:QuerySet = queryset.filter(condition_primary)
        if not queryset.exists():
            return queryset
        excludes = set()
        for room in queryset.all():
            if room.reservations.exists():
                target = room.reservations
                results = target.filter(condition_a|condition_b)
                if results.exists():
                    excludes.add(room.id)
                    continue
            else:
                continue
        queryset = queryset.exclude(id__in=excludes)
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
        pk = self.kwargs.get("pk", None)
        queryset = RoomReservation.objects.filter(id=pk)
        return queryset

    @response_error_handler
    def get(self, request, *args, **kwargs):
        if request.user.id in (
            self.get_queryset()[0].user.id,
            self.get_queryset()[0].room.host.id,
        ):
            return super().get(request, *args, **kwargs)
        raise PermissionError(
            "only owner of reservation or host of room could do this", "dont do it"
        )

    @response_error_handler
    def put(self, request, *args, **kwargs):
        if not (request.user.id == self.get_queryset()[0].user.id):
            raise PermissionError(
                "only Owner of reservation could do this", "dont do it"
            )
        if self.get_queryset()[0].start_date >= datetime.now().date():
            raise ValueError(
                "start date not passed", "evaluate your reservation after first-day"
            )
        super().put(request, *args, **kwargs)
        room_id = int(self.get_queryset()[0].room_id)
        target = RoomReservation.objects.filter(room=room_id)
        totals = target.aggregate(
            Avg("accuracy_score"),
            Avg("location_score"),
            Avg("communication_score"),
            Avg("checkin_score"),
            Avg("clean_score"),
            Avg("value_score"),
        )
        total = 0
        room = Room.objects.filter(id=room_id)
        updates = dict()
        for key, val in totals.items():
            total += val
            updates.setdefault(key[:-5], round(val, 2))

        total = round(total / 6, 2)
        room.update(**updates, total_rating=total)
        return Response(data=updates, status=status.HTTP_202_ACCEPTED)


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
        pk=int(self.kwargs.get("pk"))
        stayables = reservation_validation(Room.objects.all(), start_date, end_date)
        if Room.objects.get(id=pk) in stayables:
            return super().post(request, *args, **kwargs)
        else:
            raise ValueError("Date already reservated!", "check for another date.")

