from config.utils import response_error_handler
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.db.models import Avg, Q
from rest_framework.permissions import AllowAny, IsAuthenticated


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
    additional_serializer_class = RepresentationTripSerializer
    global_adventure_trip_serializer_class = MainGlobalTrip
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

    # 여기서 부터 글로벌 트립 이것이 글로벌 트립
    def get_global_trip_queryset(self):
        return Trip.objects.all().order_by("?")[:13]


    def get_main_trip_queryset(self):
        return Trip.objects.filter(sub_category__category__name="어드벤쳐").order_by("?")[:7]

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

    def get_additional_queryset(self):
        return Trip.objects.filter(main_page=True)

    def get_additional_serializer_class(self):
        assert self.additional_serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        return self.additional_serializer_class

    def get_additional_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_additional_serializer(self, *args, **kwargs):
        additional_serializer_class = self.get_additional_serializer_class()
        kwargs['context'] = self.get_additional_serializer_context()
        return additional_serializer_class(*args, **kwargs)

    #글로벌 트립 분기를 위해서 추가 메서드 작성
    def get_global_adventure_trip_serializer_class(self):
        assert self.global_adventure_trip_serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        return self.global_adventure_trip_serializer_class

    def get_global_adventure_trip_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_global_adventure_trip_serializer(self, *args, **kwargs):
        global_adventure_trip_serializer_class = self.get_global_adventure_trip_serializer_class()
        kwargs['context'] = self.get_additional_serializer_context()
        return global_adventure_trip_serializer_class(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        # 지역에 관한 스테이트
        queryset = self.filter_queryset(self.get_state_queryset())
        serializer = self.get_state_serializer(queryset, many=True)
        # 여기서 부터 글로벌 트립
        queryset2 = self.filter_queryset(self.get_global_trip_queryset())
        serializer2 = self.get_global_trip_serializer(queryset2, many=True)
        queryset3 = self.filter_queryset(self.get_main_trip_queryset())
        serializer3 = self.get_global_adventure_trip_serializer(queryset3, many=True)
        queryset4 = self.filter_queryset(self.get_additional_queryset())
        serializer4 = self.get_additional_serializer(queryset4, many=True)
        context = {
            "representation_trip_5": serializer4.data,
            "main_categories": response.data,
            "global_adventure_trip": serializer3.data,
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
    reservation_queryset = Reservation.objects.all()
    reservation_serializer_class = TripReservationCreateSerializer
    name = 'trip-detail'

    def get_reservation_queryset(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        user = self.request.user
        return Reservation.objects.all().filter(user_set=user.id, trip_schedule__trip_set=filter_kwargs["pk"])

    def get_reservation_serializer_class(self):
        assert self.reservation_serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        return self.reservation_serializer_class

    def get_reservation_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_reservation_serializer(self, *args, **kwargs):
        reservation_serializer_class = self.get_reservation_serializer_class()
        kwargs['context'] = self.get_reservation_serializer_context()
        return reservation_serializer_class(*args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance2 = self.filter_queryset(self.get_reservation_queryset())
        serializer = self.get_serializer(instance)
        serializer2 = self.get_reservation_serializer(instance2, many=True)

        context = {
            "trip_detail": serializer.data,
            "my_reservation": serializer2.data,

        }
        return Response(context)


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

    def perform_create(self, serializer):
        serializer.save(user_set=self.request.user)
        guest_count = serializer.data["guest_count"]
        schedule = serializer.data["trip_schedule"]
        # 트립 스케줄의 인원수 업데이트
        schedule = TripSchedule.objects.get(pk=schedule)
        schedule_now_guest_count = schedule.now_guest_count
        schedule.now_guest_count = schedule_now_guest_count + guest_count
        if schedule.capacity == schedule.now_guest_count:
            schedule.active = False
        schedule.save()

    def post(self, request, *args, **kwargs):
        trip_schedule = request.data["trip_schedule"]
        guest_count = request.data["guest_count"]
        if self.reservation_checker(guest_count, trip_schedule):
            return super().post(request, *args, **kwargs)
        raise ValueError("인원수가 맞지 않습니다", "인원수를 확인 해주세요")


class TripReservationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = TripReservationCreateSerializer
    name = "reservation-detail"


class TripReviewCreate(generics.ListCreateAPIView):
    """
    리뷰 만들때 POST
    trip_set = 트립의아이디
    reservation_set = 유저의 예약정보
    description = 유저의 후기
    rating_socre = 점수 1~5점 사이
    """

    queryset = TripReview.objects.all()
    serializer_class = TripReviewSerializer
    name = "trip-review"

    def perform_create(self, serializer):
        serializer.save(user_set=self.request.user)
        trip = serializer.data["trip_set"]
        trip = Trip.objects.get(pk=trip)
        trip_all_review = TripReview.objects.filter(trip_set=trip)
        trip_avg_score = trip_all_review.aggregate(Avg("rating_score"))
        trip.rating_score = trip_avg_score["rating_score__avg"]
        trip.save()


class TripScheduleList(generics.ListCreateAPIView):
    """
    capacity - now_guest_count 를 빼서
    사용자에게 현재 예약 가능 인원을 제공해주시면 됩니다.
    """
    queryset = TripSchedule.objects.all()
    serializer_class = TripScheduleSerializer
    name = "trip-schedule-list"


class TripLikeListView(generics.ListAPIView):
    serializer_class = TripLikeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = TripLike.objects.filter(Q(user=self.request.user))
        return queryset


class TripLikeCreateView(generics.CreateAPIView):
    serializer_class = TripLikeCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = TripLike.objects.filter(Q(user=self.request.user))
        return queryset

    @response_error_handler
    def perform_create(self, serializer: TripLikeSerializer):
        pk = int(self.kwargs.get("pk", None))
        if self.get_queryset().filter(Q(trip=Trip.objects.get(id=pk))):
            raise ValueError("already have!", "unlike Trip or like others")
        return TripLike.objects.create(user=self.request.user, trip=Trip.objects.get(id=pk))


class TripLikeDestroyView(generics.DestroyAPIView):
    serializer_class = TripLikeCreateSerializer
    permission_classes = (IsAuthenticated,)

    @response_error_handler
    def get_object(self):
        pk = int(self.kwargs.get("pk", None))
        quer = TripLike.objects.filter(Q(user=self.request.user) & Q(trip=Trip.objects.get(id=pk)))
        if not quer:
            raise ValueError(f"trip on {pk} not on your likes", "recheck your like list.")
        return quer[0]


class ApiRoot(generics.GenericAPIView):
    """
    트립 API 상세 설명
    main/ - > 트립의 메인페이지 구성을 위한 전체 요소
    trip-category - > 트립의 대분류 카테고리 목록
    trip-category/int/ - > 트립의 대분류 카테고리 상세뷰
    trips/ -> 트립의 전체 목록
    trips/int/ -> 트립의 상세뷰
    schedule/ -> 트립의 스케줄 리스트
    state - > 지역구분
    state/<int:pk> -> 지역별 상세뷰



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
            "review": reverse(TripReviewCreate.name, request=request),

        })


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import scrapy
import selenium
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import random


def crawling(request):
    # txt_total = 430
    # f = open("output.txt")
    # for _ in range(txt_total):
    #     target = f.readline().strip
    driver = webdriver.Chrome()
    driver.get(
        "https://www.airbnb.co.kr/experiences/387627?salt=ee0c9d12-1860-4084-a4e9-7a1863058336")
    sleep(3.0)

    for _ in range(7):
        driver.find_element_by_xpath(
            '//*[@id="Section16"]/div/div/div/section/div/div[1]/div/div/div/div/aside/div[2]/div/div/div[1]/div/button[2]').click()
        sleep(1.5)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(3)
    trip_scrapy_selector = Selector(text=driver.page_source)
    # 디테일 카테고리
    detail_category = trip_scrapy_selector.xpath(
        '//*[@id="Section16"]/div/div/div/section/div/div[2]/section/div[1]/div[1]/div/text()').extract_first()
    print("1", end=" ")
    print(detail_category)
    # 타이틀
    name = trip_scrapy_selector.xpath(
        '//*[@id="Section16"]/div/div/div/section/div/div[2]/section/div[1]/div[2]/div/div/h2/div/text()').extract_first()
    print("2", end=" ")
    print(name)
    # 스테이트 추후 보완 지역으로 임의 지정
    state = trip_scrapy_selector.xpath(
        '//*[@id="Section16"]/div/div/div/section/div/div[2]/section/div[2]/div/div[2]/div/button/text()').extract_first()
    print("3")
    print(state)
    # 소요시간 나중에 숫자만 빼야됨
    duration = trip_scrapy_selector.xpath(
        '//*[@id="Section16"]/div/div/div/section/div/div[2]/section/div[3]/div/div[2]/div/text()'
    ).extract_first()
    print("4")
    print(duration)
    # 제공항목 ex) 음식, 음료 - 리스트
    provide = trip_scrapy_selector.xpath(
        '//*[@id="Section16"]/div/div/div/section/div/div[2]/section/div[4]/div/div[2]/div/text()').extract_first()
    print("5", end=" ")
    provide = provide.split(",")
    print(provide)
    print(len(provide))
    # 제공 언어 - 리스트
    language = trip_scrapy_selector.xpath(
        '//*[@id="Section16"]/div/div/div/section/div/div[2]/section/div[5]/div/div[2]/div/text()').extract_first()
    print(language)
    # 호스트 소개
    host_description = trip_scrapy_selector.xpath(
        '//*[@id="Section16"]/div/div/div/section/div/div[2]/section/div[8]/div[1]/div[2]/div/div/div/div/text()').extract_first()
    if host_description == None:
        host_description = trip_scrapy_selector.xpath(
            '//*[@id="Section16"]/div/div/div/section/div/div[2]/section/div[9]/div[1]/div[2]/div/div/div/div/text()'
        ).extract_first()
    print("6", end=" ")
    print(host_description)
    # 프로그램
    program = trip_scrapy_selector.xpath(
        '//*[@id="Section16"]/div/div/div/section/div/div[2]/section/div[10]/div[1]/div[2]/div/div/div/div/text()').extract_first()
    if program == None:
        program = trip_scrapy_selector.xpath(
            '//*[@id="Section16"]/div/div/div/section/div/div[2]/section/div[11]/div[1]/div[2]/div/div/div/div/text()'
        ).extract_first()
    print("7", end=" ")
    print(program)
    # program = program[0]
    # 추가사항
    additional_condition = trip_scrapy_selector.xpath(
        '//*[@id="Section16"]/div/div/div/section/div/div[2]/section/div[12]/div[1]/div[2]/div/div/text()').extract_first()
    if additional_condition == None:
        additional_condition = trip_scrapy_selector.xpath(
            '//*[@id="Section16"]/div/div/div/section/div/div[2]/section/div[13]/div[1]/div[2]/div/div/text()'
        ).extract_first()
    print("8", end=" ")
    print(additional_condition)

    # 제공항목에 대한 상세사항
    # 제공항목 갯수에 따라 디스크립션 수집 갯수가 변하도록 함.
    provide_description_list = []
    front_xpath = '//*[@id="Section16"]/div/div/div/section/div/div[2]/section/div[14]/div[1]/div[2]/div/div/div['
    back_xpath = ']/div[2]/div/text()'
    print(len(provide))
    for count in range(len(provide)):
        in_count = str(count + 1)
        full_xpath = front_xpath + in_count + back_xpath
        count += 1
        provide_description = trip_scrapy_selector.xpath(full_xpath).extract_first()
        provide_description_list.append(provide_description)

    print(provide_description_list)
    if provide_description_list[1] == None:
        front_xpath = '//*[@id="Section16"]/div/div/div/section/div/div[2]/section/div[15]/div[1]/div[2]/div/div/div['
        back_xpath = ']/div[2]/div/text()'
        provide_description_list = []

        for count in range(1,len(provide)+1):
            in_count = str(count)
            full_xpath = front_xpath + in_count + back_xpath

            provide_description = trip_scrapy_selector.xpath(full_xpath).extract_first()
            provide_description_list.append(provide_description)

        print(provide_description_list)

    # provide_xpath = '//*[@id="Section16"]/div/div/div/section/div/div[2]/section/div[14]/div[1]/div[2]/div/div/div[1]/div[2]/div/text()'
    # provide_description = trip_scrapy_selector.xpath(
    #     '//*[@id="Section16"]/div/div/div/section/div/div[2]/section/div[14]/div[1]/div[2]/div/div/div[1]/div[2]/div/text()').extract_first()
    # print(provide_description)
    image_1 = trip_scrapy_selector.xpath(
        '//*[@id="Section16"]/div/div/div/section/div/div[1]/div/div/div/div/aside/div[1]/div/div[1]/div/div/img/@src'
    ).extract_first()
    print(image_1)
    if image_1 == None:
        image_1= "없음"
    else:
        image_1 = image_1.split("?")
        image_1 = image_1[0]
    image_2 = trip_scrapy_selector.xpath(
        '//*[@id="Section16"]/div/div/div/section/div/div[1]/div/div/div/div/aside/div[1]/div/div[2]/div/div/img/@src'
    ).extract_first()
    print(image_2)
    if image_2 == None:
        image_2= "없음"
    else:
        image_2 = image_2.split("?")
        image_2 = image_2[0]
    image_3 = trip_scrapy_selector.xpath(
        '//*[@id="Section16"]/div/div/div/section/div/div[1]/div/div/div/div/aside/div[1]/div/div[3]/div/div/img/@src'
    ).extract_first()
    print(image_3)
    if image_3 == None:
        image_3= "없음"
    else:
        image_3 = image_3.split("?")
        image_3 = image_3[0]
    image_4 = trip_scrapy_selector.xpath(
        '//*[@id="Section16"]/div/div/div/section/div/div[1]/div/div/div/div/aside/div[1]/div/div[4]/div/div/img/@src'
    ).extract_first()
    print(image_4)
    if image_4 == None:
        image_4= "없음"
    else:
        image_4 = image_4.split("?")
        image_4 = image_4[0]
    image_5 = trip_scrapy_selector.xpath(
        '//*[@id="Section16"]/div/div/div/section/div/div[1]/div/div/div/div/aside/div[1]/div/div[5]/div/div/img/@src'
    ).extract_first()
    print(image_5)
    if image_5 == None:
        image_5= "없음"
    else:
        image_5 = image_5.split("?")
        image_5 = image_5[0]
    image_6 = trip_scrapy_selector.xpath(
        '//*[@id="Section16"]/div/div/div/section/div/div[1]/div/div/div/div/aside/div[1]/div/div[6]/div/div/img/@src'
    ).extract_first()
    if image_6 == None:
        image_6= "없음"
    else:
        image_6 = image_6.split("?")
        image_6 = image_6[0]
    print(image_6)
    image_7 = trip_scrapy_selector.xpath(
        '//*[@id="Section16"]/div/div/div/section/div/div[1]/div/div/div/div/aside/div[1]/div/div[7]/div/div/img/@src'
    ).extract_first()
    print(image_7)
    if image_7 == None:
        image_7= "없음"
    else:
        image_7 = image_7.split("?")
        image_7 = image_7[0]

    place_info = trip_scrapy_selector.xpath(
        '//*[@id="Section9"]/div/div/div/section/div/div[2]/section/div/text()'
    ).extract_first()
    print(place_info)
    # 위도, 경도
    address = trip_scrapy_selector.xpath(
        '//*[@id="site-content"]/div/div[2]/div[2]/div[1]/div/div[6]/div/div/div/div[1]/div/div/div[2]/a/@href'
    ).extract_first()
    # 위도 경도가 시작 되는 부분을 찾아서 슬라이싱 후 float로 변환
    address = address[address.find("=") + 1:address.find("&")]
    address = address.split(",")
    latitude = float(address[0])
    longitude = float(address[1])
    print(address)
    print(latitude)
    print(longitude)

    # 가격
    price = trip_scrapy_selector.xpath(
        '//*[@id="Section10"]/div/div/div/section/div/div[2]/section/div/div[1]/div/div/div[1]/div[2]/div/text()'
    ).extract_first()
    price = price[price.find("₩") + 1:price.find("/")]
    price_list = []
    for price_char in price:
        if price_char.isdigit():
            price_list.append(price_char)
    price_string = "".join(price_list)
    price_integer = int(price_string)
    print(price_integer)

    # 게스트 수
    max_guest = trip_scrapy_selector.xpath(
        '//*[@id="Section10"]/div/div/div/section/div/div[2]/section/div/div[1]/div/div/div[1]/div[3]/text()'
    ).extract_first()
    max_guest = max_guest[0]
    max_guest = int(max_guest)
    print(max_guest)

    # 유저 후기
    # 유저의 이미지
    user_image_front = '//*[@id="Section12"]/div/div/div/section/div/div[2]/section/div/div['
    user_image_back = ']/div[1]/div/div/div[1]/div/a/img/@src'
    # user_image = trip_scrapy_selector.xpath(
    #     '//*[@id="Section12"]/div/div/div/section/div/div[2]/section/div/div[1]/div[1]/div/div/div[1]/div/a/img/@src'
    # ).extract_first()
    # print(user_image)

    # 후기 포스팅 날짜
    # review_date_front = '//*[@id="Section12"]/div/div/div/section/div/div[2]/section/div/div['
    # review_date_back = ']/div[1]/div/div/div[2]/div/div[1]/div/span/text()'
    # review_date = trip_scrapy_selector.xpath(
    #     '//*[@id="Section12"]/div/div/div/section/div/div[2]/section/div/div[1]/div[1]/div/div/div[2]/div/div[1]/div/span/text()'
    # ).extract_first()
    # print(review_date)

    # 유저 네임
    username_front = '//*[@id="Section12"]/div/div/div/section/div/div[2]/section/div/div['
    username_back = ']/div[1]/div/div/div[2]/div/div[1]/div/a/span/text()'
    # username = trip_scrapy_selector.xpath(
    #     '//*[@id="Section12"]/div/div/div/section/div/div[2]/section/div/div[1]/div[1]/div/div/div[2]/div/div[1]/div/a/span/text()'
    # ).extract_first()
    # print(username)

    # 리뷰 후기
    review_description_front = '//*[@id="Section12"]/div/div/div/section/div/div[2]/section/div/div['
    review_description_back = ']/div[2]/div/div/text()'
    # review_description = trip_scrapy_selector.xpath(
    #     '//*[@id="Section12"]/div/div/div/section/div/div[2]/section/div/div[1]/div[2]/div/div/text()'
    # ).extract_first()
    # print(review_description)

    # 리뷰 점수
    review_score_front = '//*[@id="Section12"]/div/div/div/section/div/div[2]/section/div/div['
    review_score_bakc = ']/div[1]/div/div/div[2]/div/div[2]/span/@aria-label'
    # review_score = trip_scrapy_selector.xpath(
    #     '//*[@id="Section12"]/div/div/div/section/div/div[2]/section/div/div[1]/div[1]/div/div/div[2]/div/div[2]/span/@aria-label'
    # ).extract_first()
    # print(review_score)
    # total_score = trip_scrapy_selector.xpath(
    #     '//*[@id="Section12"]/div/div/div/section/div/div[1]/div/div[2]/div/div/div/test()'
    # ).extract_first()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time = [1, 2, 3, 4, 5]
    score = [4.6, 4.7, 4.8, 4.9, 5.0]
    duration = random.choice(time)
    # 서버족은 user 14 sub 7 state 2
    trip = Trip.objects.create(host=User.objects.get(pk=1),
                               name=name,
                               sub_category=SubTripCategory.objects.get(pk=1),
                               detail_category=detail_category,
                               state=State.objects.get(pk=1),
                               duration_time=duration,
                               host_about=host_description,
                               program=program,
                               place_info=place_info,
                               latitude=latitude,
                               longitude=longitude,
                               guest_material="선택사항",
                               min_age=18,
                               compatibility="YES",
                               strength="LIGHT",
                               technic="BEGINNER",
                               additional_condition=additional_condition,
                               certification=False,
                               max_guest=max_guest,
                               price=price_integer,
                               rating_score=4.9,
                               representation=False,
                               language=language,
                               image_1=image_1,
                               image_2=image_2,
                               image_3=image_3,
                               image_4=image_4,
                               image_5=image_5,
                               image_6=image_6,
                               image_7=image_7,
                               )
    print("*********************")
    provide_count = len(provide)
    provide_list = provide
    num = 0
    while True:
        if num == provide_count - 1:
            break
        provide = provide_list[num]
        print(provide)
        if len(Provide.objects.filter(name=provide)) != 0:
            provide = Provide.objects.get(name=provide)
            TripProvide.objects.create(trip_set=trip, provide_set=provide, description=provide_description_list[num])
            num += 1
            if num == provide_count -1:
                break
        else:
            provide = Provide.objects.create(name=provide)
            TripProvide.objects.create(trip_set=trip, provide_set=provide, description=provide_description_list[num])
            num += 1
            if num == provide_count - 1:
                break

    try:
        next_button = driver.find_element_by_xpath(
            '//*[@id="Section12"]/div/div/div/section/div/div[2]/section/div/div[6]/nav/span/div/ul/li[6]/button')
    except:
        print("gg")
        try:
            for review_count in range(1, 6):
                review_count = str(review_count)
                # 유저 이미지
                user_image_complete = user_image_front + review_count + user_image_back
                user_image = trip_scrapy_selector.xpath(user_image_complete).extract_first()
                print(user_image)

                # 후기 포스팅 날짜
                # review_date_complete = review_date_front + review_count + review_date_back
                # review_date = trip_scrapy_selector.xpath(review_date_complete).extract_first()
                # print(review_date)

                # 유저네임
                username_complete = username_front + review_count + username_back
                username = trip_scrapy_selector.xpath(username_complete).extract_first()
                username = username.lower()
                if " " in username:
                    username = username.split(" ")
                    username = "".join(username)
                print(username)

                # 리뷰 후기에 관한
                review_description_complete = review_description_front + review_count + review_description_back
                review_description = trip_scrapy_selector.xpath(review_description_complete).extract_first()
                print(review_description)

                # 리뷰 점수에 관한 것
                review_score_complete = review_score_front + review_count + review_score_bakc
                review_score = trip_scrapy_selector.xpath(review_score_complete).extract_first()
                score_check = review_score.find("/")
                score = review_score[score_check - 1]

                user = User.objects.create_user(username=username,
                                                password="anffp7844",
                                                trip_image=user_image,)
                review = TripReview.objects.create(
                    user_set=user,
                    trip_set=trip,
                    description=review_description,
                    rating_score=score,
                )

                print(score)
        except:
            print("리뷰 갯수 부족")
            print("다음 가기 버튼이 없습니다.")
    sleep(2.5)

    # 리뷰 총 페이지의 사이즈 계산
    try:
        review_page_max = trip_scrapy_selector.xpath(
            '//*[@id="Section12"]/div/div/div/section/div/div[2]/section/div/div[6]/nav/span/div/ul/li[5]/button/div/text()'
        ).extract_first()
        review_page_max = 4
        print(review_page_max)
        for x in range(review_page_max):
            next_button.click()
            sleep(3)
            try:
                for review_count in range(1, 6):
                    review_count = str(review_count)
                    # 유저 이미지
                    user_image_complete = user_image_front + review_count + user_image_back
                    user_image = trip_scrapy_selector.xpath(user_image_complete).extract_first()
                    print(user_image)

                    # 후기 포스팅 날짜
                    # review_date_complete = review_date_front + review_count + review_date_back
                    # review_date = trip_scrapy_selector.xpath(review_date_complete).extract_first()
                    # print(review_date)

                    # 유저네임
                    username_complete = username_front + review_count + username_back
                    username = trip_scrapy_selector.xpath(username_complete).extract_first()
                    username = username.lower()
                    if " " in username:
                        username = username.split(" ")
                        username = "".join(username)
                    print(username)

                    # 리뷰 후기에 관한
                    review_description_complete = review_description_front + review_count + review_description_back
                    review_description = trip_scrapy_selector.xpath(review_description_complete).extract_first()
                    print(review_description)

                    # 리뷰 점수에 관한 것
                    review_score_complete = review_score_front + review_count + review_score_bakc
                    review_score = trip_scrapy_selector.xpath(review_score_complete).extract_first()
                    score_check = review_score.find("/")
                    score = review_score[score_check - 1]

                    user = User.objects.create_user(username=username,
                                                    password="anffp7844",
                                                    trip_image=user_image,
                                                    )
                    review = TripReview.objects.create(
                        user_set=user,
                        trip_set=trip,
                        description=review_description,
                        rating_score=score,
                    )

                    print(score)
            except:
                print("리뷰 갯수 부족")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(x)
    except:
        print("페이지 사이즈가 존재하지 않습니다. 덧글 끝가지 돌았습니다.")

    driver.close()


