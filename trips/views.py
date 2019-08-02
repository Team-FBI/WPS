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
        trip_queryset = Trip.objects.all().filter(state_id=filter_kwargs["pk"]).order_by("?")[:13]
        max_id = trip_queryset.count()
        # random_queryset = Trip.objects.none()
        # while True:
        #     random_index = random.randint(0, max_id)
        #     random_queryset = trip_queryset[random_index:random_index + 1]
        #     if random_queryset.count() == 1:
        #         break order_by("?)
        return trip_queryset

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


class TripMain(generics.ListCreateAPIView):
    """
    트립의 메인 페이지 정보
    main_categories : 어드벤쳐, 식도락여행, 역사투어, 쿠킹 클래스, 착한 드립 5개의 메인 대분류 코테고리 분류.
    global_recommend_trip : 전체 트립 목록 중 임의의 13개 트립 제공.
    -> 미제공 사항 : 트립의 리뷰카운터, 진행언어 - > 추후 업데이트
    state : trip데이터가 존재하는 state 8개 state의 이미지는 별도로 셋팅 부탁 드립니다.
    """
    queryset = TripCategory.objects.all()
    serializer_class = TripCategorySerializer
    state_queryset = State.objects.all()
    state_serializer_class = TripStateSerializer
    global_trip_queryset = Trip.objects.all()
    global_trip_serializer_class = TripCategoryOnly
    name = 'trip-main'

    def get_state_queryset(self):
        state = State.objects.exclude(trips__isnull=True)
        return state

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

    # 여기서 부터 글로벌 트립
    def get_global_trip_queryset(self):
        return Trip.objects.all().order_by("?")[:13]

    def get_global_trip_serializer_class(self):
        assert self.global_trip_serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        return self.global_trip_serializer_class

    def get_global_trip_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_global_trip_serializer(self, *args, **kwargs):
        global_trip_serializer_class = self.get_global_trip_serializer_class()
        kwargs['context'] = self.get_state_serializer_context()
        return global_trip_serializer_class(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        # 지역에 관한 스테이트
        queryset = self.filter_queryset(self.get_state_queryset())
        serializer = self.get_state_serializer(queryset, many=True)
        # 여기서 부터 글로벌 트립
        queryset2 = self.filter_queryset(self.get_global_trip_queryset())
        serializer2 = self.get_global_trip_serializer(queryset2, many=True)
        # queryset3 = self.filter_queryset((self.get_queryset()))

        context = {
            "main_categories": response.data,
            "global_recommend_trip": serializer2.data,
            "state": serializer.data,

        }
        return Response(context)


class TripCategoryList(generics.ListCreateAPIView):
    """
    trip/trip-category/<int:pk>/ pk에 정수를 넣어서 카테고리 상세조회 가능.
    그러나 대분류 카테고리별 분류에서 어드벤쳐 트립 정보를 가져가시면 됩니다.
    카테고리에서 제공하는 필드값은 list, detail 뷰 동일함.
    name : 대분류 카테고리 이름
    image : 대분류 이미지 사진 한장
    description : 대분류 카테고리에 해당 하는 설명
    """
    queryset = TripCategory.objects.all()
    serializer_class = TripCategorySerializer
    name = 'tripcategory-list'


class TripCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TripCategory.objects.all()
    serializer_class = TripCategoryDetailSerializer
    state_queryset = State.objects.all()
    state_serializer_class = TripStateSerializer
    name = 'tripcategory-detail'


class TripList(generics.ListCreateAPIView):
    """
    전체 트립 리스트를 제공
    trip/<int:pk>/ 정수 제공시 트립의 뷰로 이동
    ***미제공 사항 리뷰카운터, 진행언어
    name : 트립의 제목
    image_1 : 대표 이미지
    duration_time : 트립의 진행시간
    provides : 트립에서 제공 하는 것
    url : 상세페이지 url 아이디값을 포함하고 있음.
    """
    queryset = Trip.objects.all()
    serializer_class = TripListSerializer
    name = 'trip-list'


class TripDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    트립의 상세페이지
    앱에서 보이는 순서대로 정렬 하여 제공.
    "name" : 트립의 제목
    "sub_category : 대분류 카테고리:어드벤쳐 - > 서브 카테고리: 파리의 어드벤처 <지역이 붙은 소분류 카테고리
    "state" : 지역
    "duration_time" : 진행시간
    "provides", : 제공 항목
    "schedules", : 예약 가능한 스케줄
    "trip_reviews" : 현재 트립의 리뷰
    "host" : 호스트 이름
    "host_about" : 호스트 소개
    "program" : 프로그램에 관한 설명
    "additional_condition" : 추가 조건에 관한 텍스틔 필드
    "guest_material" : 게스트 준비물
    "address" : 지도 검색을 위한 주소
    "place_info" : 장소에 관한 설명
    "min_age" : 최소 나이 조건
    "max_guest" : 최대 수용인원
    "certification" : 신분증 지참여부 True-필요 False-불필요
    "price" : 1인당 가격
    "rating_score" : 트립의 총 리뷰 점수 평균
    "compatibility" : 장애인 이용 가능 여부
    "strength" : 트립의 강도
    "technic" : 트립을 즐기는데 필요한 테크닉의 정도
    "image_1",
    "image_2",
    "image_3",
    "image_4",
    "image_5",
    "image_6",
    "image_7",
    """
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    name = 'trip-detail'


class TripReservationCreate(generics.ListCreateAPIView):
    """
    POST
    "guest_count": 예약 할 인원수
    "total_price": 토탈 가격
    "trip_set": 트립 아이디
    "trip_schedule": 트립의 스케줄 아이디
    """
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


class TripScheduleList(generics.ListCreateAPIView):
    """
    capacity - now_guest_count 를 빼서
    사용자에게 현재 예약 가능 인원을 제공해주시면 됩니다.
    """
    queryset = TripSchedule.objects.all()
    serializer_class = TripScheduleSerializer
    name = "trip-schedule-list"

    # def post(self, request, *args, **kwargs):
    #     # trip = request.data["trip_set"]
    #     # reservation = request.data["reservation_set"]
    #     return super().post(request, *args, **kwargs)

    # trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trip_reviews")
    # reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="trip_reviews")
    # description = models.TextField(blank=True)
    # rating_score = models.SmallIntegerField(default=5)


class ApiRoot(generics.GenericAPIView):
    """
    트립 API 상세 설명
    main/ - > 트립의 메인페이지 구성을 위한 전체 요소
    trip-category - > 트립의 대분류 카테고리 목록
    trip-category/int/ - > 트립의 대분류 카테고리 상세뷰
    trips/ -> 트립의 전체 목록
    trips/int/ -> 트립의 상세뷰
    schedule/ -> 트립의 스케줄 리스트


   """
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'main': reverse(TripMain.name, request=request),
            'trip-category': reverse(TripCategoryList.name, request=request),
            'trips': reverse(TripList.name, request=request),
            'schedule': reverse(TripScheduleList.name, request=request),
            "reservation": reverse(TripReservationCreate.name, request=request),
            "state": reverse(StateList.name, request=request),
            "review": reverse(TripReviewCreate.name, request=request)

        })
