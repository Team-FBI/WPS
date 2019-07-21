from django.db.models import Q
from rest_framework.viewsets import generics
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rooms.models import Room, Reservation
from rooms.serializers import (
    RoomListSerializer,
    RoomCreateSerializer,
    RoomDetailSerializer,
    ReservationCreateSerializer,
)
from config.utils import response_error_handler

class PriceFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        min_price = request.query_params.get("min_price", 0)
        max_price = request.query_params.get("max_price", None)
        condition_min = Q(price__gte=min_price)
        if not max_price:
            return queryset.filter(condition_min)
        condition_max = Q(price__lte=max_price)
        return queryset.filter(condition_min & condition_max)


class StandardResultSetPagination(PageNumberPagination):
    page_size = 12
    max_page_size = 100
    page_query_param = "page"
    page_size_query_param = "page_size"


class RoomListView(generics.ListAPIView):
    """A function, able to get list of Room
    - GET[list]
    Arguments:
        viewsets {[ListAPIView]} -- [GET handler]
    QuerystringOptions:
    #ordering-required
        ordering -- [default update_at, price, updated_at, created_at, total_rating]
        page_size -- [default 12, data amount in page]
        page -- [default 1, page of data-perpage]

    #filterings-required
        search -- [could come state or country or part of host email]

    #filterings-Non_required
        min_price -- [default All, filter price greater than input]
        max_price -- [default All, filter price lower than input]
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
    pagination_class = StandardResultSetPagination
    queryset = Room.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, PriceFilterBackend]
    search_fields = ["=state__name", "=state__country__name", "^host__username"]
    ordering_fields = ["price", "created_at", "updated_at", "total_rating"]
    ordering = ["updated_at"]

    @response_error_handler
    def get(self, request, *args, **kwargs):
        # print(request.query_params)
        query_order = request.query_params.get("ordering")
        query_search = request.query_params.get("search")
        page = request.query_params.get("page")
        page_size = request.query_params.get("page_size")
        if not all([query_search, query_order, page, page_size]):
            raise AttributeError("all Query string not specified", "?ordering=price")
        if query_order not in self.ordering_fields:
            raise AttributeError(
                "query of ordering not matched", f"specify in {self.ordering_fields}"
            )
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
        if not (queryset[0] and room_id):
            raise ValueError("Room id Not Found", "check room id")
        return queryset

    @response_error_handler
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


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


######## 토요일 추가
from .serializers import *
from rest_framework import status


class CreateRoomReview(generics.CreateAPIView):

    serializer_class = RoomReviewCreateSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.use
        reservation_id = self.kwargs.get("pk")
        reservation = Reservation.objects.get(pk=reservation_id)
        room = reservation.room_for
        if not RoomReview.objects.filter(reservation_for=reservation).exists():
            serializer = RoomReviewCreateSerializer(
                data=request.data,
                user=user,
                place_for=room,
                reservation_for=reservation,
            )
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "이미 후기를 작성하였습니다."})


class RoomReviewListView(generics.ListAPIView):

    queryset = RoomReview.objects.filter(active=True)
    serializer_class = RoomReviewListSerializer


class RoomReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update, and Delete comment endpoint
    Allowed request method: Get, Post, Delete
    """

    queryset = RoomReview.objects.all()
    serializer_class = RoomReviewDetailSerializer
