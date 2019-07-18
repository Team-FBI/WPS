from django.db.models import Q
from rest_framework.viewsets import generics
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Room, Reservation
from rooms.serializers import (
    RoomListSerializer,
    RoomCreateSerializer,
    RoomDetailSerializer,
    ReservationCreateSerializer,
)
from config.utils import response_error_handler


def filter_backend(queryset, query_params):
    order = query_params.get("order", "created_at")
    perpage = int(query_params.get("perpage", 10))
    page = int(query_params.get("page", 1))
    queryset = queryset.order_by(order)

    min_price = query_params.get("min_price", None)
    max_price = query_params.get("max_price", None)
    capacity = query_params.get("capacity", None)

    try:
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if capacity:
            queryset = queryset.filter(capacity__gte=capacity)
    except Exception:
        raise AttributeError("filter attribute error", "querystrng wasnt good")
    paged = queryset[(perpage * page - perpage) : (perpage * page)]
    if len(paged):
        return paged
    return queryset


class RoomListView(generics.ListAPIView):
    """A function, able to get list of Room
    - GET[list]
    Arguments:
        viewsets {[ListAPIView]} -- [GET handler]
    QuerystringOptions:
        #ordering
        order -- [default created_at, order by numeric values with "-" mark]
        perpage -- [default 10, data amount in page]
        page -- [default 0, page of data-perpage]

        #filterings
        state|country -- [default All, filter by state or country]
        host -- [default All, filter by host username]
        min_price -- [default All, filter price greater than input]
        max_price -- [default All, filter price lower than input]
        capacity -- [default All, filter capacity greater than input]
    Raises:
        AttributeError: [GET-HTTP_400_BAD_REQUEST]
    Returns:
        [GET-status] -- [GET-200-HTTP_200_OK]

    - POST(create)
    A function, able to Post and register new Room
    
    Arguments:
        viewsets {[CreateAPIView]} -- [POST, handler]
    
    Raises:
        ValidationError: [POST-HTTP_400_BAD_REQUEST]
        PermissionError: [POST-HTTP_401_UNAUTHORIZED]
    Returns:
        [status] -- [POST-201_CREATED]
    """

    serializer_class = RoomListSerializer

    def get_queryset(self):
        queryset = Room.objects.all()
        state = self.request.query_params.get("state", None)
        country = self.request.query_params.get("country", None)
        host = self.request.query_params.get("host", None)
        if state:
            queryset = queryset.filter(state__name=state)
        elif country:
            queryset = queryset.filter(state__country__name=country)
        if host:
            queryset = queryset.filter(host__username=host)
        queryset = filter_backend(queryset, self.request.query_params)
        return queryset

    @response_error_handler
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RoomCreateView(generics.CreateAPIView):
    """A function, able to Post and register new Room
    
    Arguments:
        viewsets {[CreateAPIView]} -- [POST, handler]
    
    Raises:
        ValidationError: [POST-HTTP_400_BAD_REQUEST]
        PermissionError: [POST-HTTP_401_UNAUTHORIZED]
    Returns:
        [status] -- [POST-201_CREATED]
    """

    serializer_class = RoomCreateSerializer
    permission_classes = (IsAuthenticated,)

    @response_error_handler
    def post(self, request, *args, **kwargs):
        condition = int(request.data.get("host", 0)) is request.user.id
        if condition:
            return super().post(request, *args, **kwargs)
        else:
            raise PermissionError(
                "Post Data User not match to Your Account",
                "Input right id of your userdata",
            )


class RoomUpdateView(generics.UpdateAPIView):
    """A function, able to put new data to update room
    
    Arguments:
        viewsets {[UpdateAPIView]} -- [PUT handler]
    Raises:
        PermissionError: [PUT_HTTP_401_UNAUTHORIZED]
        ValidationError: [PUT_HTTP_400_BAD_REQUEST]
        ValueError: [PUT_HTTP_404_NOT_FOUND]
    Returns:
        [status] -- [PUT-HTTP_204_NO_CONTENT]
    """

    serializer_class = RoomCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        pk = self.kwargs.get("pk", None)
        queryset = Room.objects.filter(id=pk)
        if not (queryset[0] and pk):
            raise ValueError("Room id Not Found", "check room id")
        return queryset

    @response_error_handler
    def put(self, request, *args, **kwargs):
        if (
            request.user == self.get_queryset()[0].host
            or request.user.is_staff
            or request.user.is_superuser
        ):
            response = super().put(request, *args, **kwargs)
            response.status_code = 204
            return response
        else:
            raise PermissionError("you are no host or staff", "dont do it")


class RoomDetailView(generics.RetrieveAPIView):
    """A function, able to GET Room Detail data
    - GET
    Arguments:
        viewsets {[RetrieveAPIView]} -- [GET handler]
    Raises:
        ValueError: [GET-HTTP_404_NOT_FOUND]
    Returns:
        [status] -- [GET-HTTP_200_OK]

    - PUT(update)
    A function, able to put new data to update room
    Arguments:
        viewsets {[UpdateAPIView]} -- [PUT handler]
    Raises:
        PermissionError: [PUT_HTTP_401_UNAUTHORIZED]
        ValidationError: [PUT_HTTP_400_BAD_REQUEST]
        ValueError: [PUT_HTTP_404_NOT_FOUND]
    Returns:
        [status] -- [PUT-HTTP_204_NO_CONTENT]

    - POST Reservation for detailed room
    "room_detail_get_url + /reservation/"
    A function, able to POST Reservation create request.
    
    Arguments:
        generics {[CreateAPIView]} -- [POST handler]
    
    Raises:
        ValueError: [POST-HTTP_404_NOT_FOUND]
        ValidationError: [POST-HTTP_400_BAD_REQUEST]

    Returns:
        [status] -- [POST-HTTP_201_CREATED]
    """

    serializer_class = RoomDetailSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        room_id = self.kwargs.get("pk", None)
        queryset = Room.objects.filter(id=room_id)
        print(queryset[0])
        if not (queryset[0] and room_id):
            raise ValueError("Room id Not Found", "check room id")
        return queryset

    @response_error_handler
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except ValueError as e:
            raise e


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

    def is_reserved_date(self, start_date, end_date):
        room_id = self.kwargs.get("pk")
        start_date_q = Q(start_date__lte=start_date, end_date__gte=start_date)
        end_date_q = Q(start_date__lte=end_date, end_date__gte=end_date)
        return (
            Reservation.objects.filter(room_id=room_id)
            .filter(end_date_q | start_date_q)
            .exists()
        )

    @response_error_handler
    def post(self, request, *args, **kwargs):
        start_date, end_date = request.data["start_date"], request.data["end_date"]
        if self.is_reserved_date(start_date, end_date):
            raise ValueError("Date already reservated!", "check for another date.")
        request.room_id = int(self.kwargs.get("pk"))

        return super().post(request, *args, **kwargs)
