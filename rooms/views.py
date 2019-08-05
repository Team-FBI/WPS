from datetime import datetime
from django.db.models import Q
from rest_framework.viewsets import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework import status
from rooms.models import Room
from rooms.serializers import (
    RoomListSerializer,
    RoomCreateSerializer,
    RoomDetailSerializer,
)
from rooms.filter_backends import (
    CapacityFilterBackend,
    DateFilterBackend,
    PriceFilterBackend,
    RatingFilterBackend
)
from reservations.views import reservation_validation
from config.utils import response_error_handler


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
        start_date, end_date -- [default None, filter date reservable, format as year-month-day]
        capacity -- [default All, filter capacity equal or larger than input]
        rating -- [default All, filter total_rating equal or larger than input]
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
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        PriceFilterBackend,
        DateFilterBackend,
        CapacityFilterBackend,
        RatingFilterBackend,
    ]
    filterset_fields = ["start_date", "end_date", "min_price", "max_price", "capacity", "rating"]
    search_fields = ["=state__name", "=state__country__name", "^host__username"]
    ordering_fields = ["price", "created_at", "updated_at", "total_rating", "-total_rating", "-price", "-created_at", "-updated_at"]
    ordering = ["updated_at"]

    @response_error_handler
    def get(self, request, *args, **kwargs):
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
    queryset = Room.objects.all()

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
        return queryset

    @response_error_handler
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
