from django.db import models
from datetime import timedelta
from .options import *
from django.contrib.auth import get_user_model

User = get_user_model()


class State(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.name


class Provide(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class TripProvide(models.Model):
    trip_set = models.ForeignKey("Trip", on_delete=models.CASCADE, related_name="provides")
    provide_set = models.ForeignKey(Provide, on_delete=models.CASCADE, related_name="trip_provides")
    description = models.TextField(default="제공하는 것에 대해 상세하게 적어주세요.")

    def __str__(self):
        return f"{self.provide_set}"


class TripCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=250)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class SubTripCategory(models.Model):
    category = models.ForeignKey(TripCategory, on_delete=models.CASCADE, related_name="sub_tripcategory")
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="sub_tripcategory")
    name = models.CharField(max_length=200, unique=True)
    image_1 = models.ImageField(blank=True)
    image_2 = models.ImageField(blank=True)
    image_3 = models.ImageField(blank=True)
    description = models.CharField(max_length=200)


class Trip(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trips")
    # 트립 제목
    name = models.CharField(max_length=200)
    trip_category = models.ForeignKey(
        TripCategory,
        on_delete=models.CASCADE,
        related_name="trips"
    )
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="trips")
    duration_time = models.SmallIntegerField(default=2)
    host_about = models.TextField(default="게스트에게 자기 소개와 함께 트립 진행에 있어 나만의 특별함을 알려주세요.")
    program = models.TextField(default="트립을 처음부터 끝까지 실제 진행 순서대로 설명해 주세요.")
    place_info = models.TextField(default="트립에서 방문할 각 장소에 대해 설명하세요.")
    address = models.CharField(max_length=250, blank=True)
    guest_material = models.CharField(max_length=250, blank=True)
    image_1 = models.ImageField(blank=True)
    image_2 = models.ImageField(blank=True)
    image_3 = models.ImageField(blank=True)
    image_4 = models.ImageField(blank=True)
    image_5 = models.ImageField(blank=True)
    image_6 = models.ImageField(blank=True)
    image_7 = models.ImageField(blank=True)
    min_age = models.PositiveIntegerField(choices=MIN_AGE, default=18)
    compatibility = models.CharField(max_length=100, choices=COMPATIBILITY, default=YES)
    strength = models.CharField(max_length=100, choices=STRENGTH, default=LIGHT)
    technic = models.CharField(max_length=100, choices=TECHNIC, default=BEGINNER)
    additional_contition = models.TextField(max_length=250, default="추가 요건(선택 사항)")
    # 신분증 지참 여부
    certification = models.BooleanField(default=False)
    max_guest = models.SmallIntegerField(choices=MAX_GUEST, default=4)
    price = models.IntegerField(default=30000)
    rating_score = models.FloatField(default=0.0)

    def trip_active(self):
        return TripSchedule.objects.filter(active=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = (
            "-rating_score",
        )


class TripSchedule(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="host_trip_schedules")
    trip_set = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="schedules")
    start_datetime = models.DateTimeField()
    user_set = models.ManyToManyField(User, blank=True, related_name="trip_schedules")
    capacity = models.IntegerField(default=0)
    now_guest_count = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def end_datetime(self):
        end_datetime = self.start_datetime + timedelta(hours=self.trip_set.duration_time)
        return end_datetime

    def __str__(self):
        return f"{self.trip_set}의 {self.start_datetime}일정"


class Reservation(models.Model):
    user_set = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trip_reservations")
    trip_set = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trip_reservations")
    trip_schedule = models.ForeignKey(TripSchedule, on_delete=models.CASCADE, related_name="trip_reservations")
    guest_count = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user_set}의 예약"


class TripReview(models.Model):
    user_set = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trip_reviews")
    trip_set = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trip_reviews")
    reservation_set = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="trip_reviews")
    description = models.TextField(blank=True)
    rating_score = models.SmallIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_set}의 리뷰"
    # 트립의 아이디, 유저의 아이디
    # 레저베이션을 찾으려면 유저의 아이디와 트립의 스케줄을 알아야 함
