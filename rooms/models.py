from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from locations.models import State
import json
import datetime
# Create your models here.



def n_tuple(n, first=[], last=[]):
    return tuple(first + [(i, i) for i in range(1, n)] + last)


NO_OF_ROOMS = n_tuple(10)
MIN_STAY = n_tuple(90)
MAX_STAY = n_tuple(60, first=[(0, "Unlimited")])
NO_OF_BEDS = n_tuple(20, first=[(0, "-")])
ROOM_RATING = n_tuple(6, first=[(0, "Not rated")])
ORDER = n_tuple(20, first=[(0, "-")])
MAX_GUEST = n_tuple(20, first=[(0, "-")])


ROOM_TYPES = [
    (1, "Apartment"),
    (2, "House"),
    (3, "Garden House"),
    (4, "Bed and Breakfast"),
    (5, "Villa"),
    (6, "Caravan"),
    (50, "Office"),
]

SPACE_TYPES = [(1, "Entire room"), (2, "Private Room"), (3, "Shared Room")]

BATHROOM_TYPES = [(1, "Private"), (2, "Shared")]

CANCELATION_RULES = [(1, "Flexible"), (2, "Semi-flexible"), (3, "Strict")]

UNAVAIL_REASON = [(1, "Unavailable"), (2, "Requested"), (3, "Booked")]

PHOTO_TYPES = [
    (1, "Inside of the room"),
    (2, "View of the room"),
    (3, "External appearance of the room"),
    (4, "Around the room"),
    (4, "Other"),
]

BOOKING_STATUS = [
    (5, "Prepared"),
    (8, "Pre Requested - Waiting for payment"),
    (9, "Pre Requested - Waiting for confirmation of payment"),
    (10, "Requested"),
    (20, "Confirmed by host"),
    (30, "Confirmed by guest"),
    (40, "Rejected by host"),
    (50, "Canceled by guest"),
    (60, "Canceled by staff"),
]

MESSAGE_STATUS = [
    (10, "Waiting for confirmation"),
    (20, "Confirmed, visible"),
    (25, "Directly send"),
    (30, "Deactived by staff"),
    (40, "Deleted"),
    (50, "Archived"),
]

REVIEW_STATUS = [
    (1, "Waiting for confirmation"),
    (2, "Confirmed, active"),
    (3, "Deactived by staff"),
    (4, "Deleted by reviewer"),
    (5, "Archived"),
]


class Room(models.Model):

    host = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="rooms"
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    address = models.CharField(max_length=250, blank=True)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING, related_name="rooms")
    postal_code = models.CharField(max_length=15, blank=True, null=True)
    mobile = models.IntegerField(blank=False, null=False)
    image = models.ImageField(upload_to=f"rooms/%Y/%m/%d/", blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, null=True)
    capacity = models.SmallIntegerField(choices=NO_OF_BEDS, default=6)
    room_type = models.SmallIntegerField(choices=ROOM_TYPES, default=1)
    space = models.SmallIntegerField(choices=SPACE_TYPES, default=1)
    bedroom = models.SmallIntegerField(choices=NO_OF_ROOMS, default=1)
    bed_type = models.SmallIntegerField(choices=BATHROOM_TYPES, default=1)
    bathroom = models.SmallIntegerField(choices=NO_OF_ROOMS, default=1)
    cancellation = models.SmallIntegerField(choices=CANCELATION_RULES, default=1)
    min_stay = models.SmallIntegerField(choices=MIN_STAY, default=1)
    max_stay = models.SmallIntegerField(choices=MAX_STAY, default=0)
    description = models.TextField(blank=True, null=True)
    accuracy_rating = models.SmallIntegerField(default=0)
    location_rating = models.SmallIntegerField(default=0)
    communication_rating = models.SmallIntegerField(default=0)
    checkin_rating = models.SmallIntegerField(default=0)
    clean_rating = models.SmallIntegerField(default=0)
    value_rating = models.SmallIntegerField(default=0)
    total_rating = models.SmallIntegerField(default=0)
    reserved_dates = models.TextField(editable=False, default="")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def save(self):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Room, self).save()

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        # get_latest_by = "timestamp"
        # verbose_name = 'room'

    def __str__(self):
        return f"{self.slug} / {self.host}"

    def reserved_update(self):
        """
        ReservedDates의 외래키 릴레이트 네임인 reserveds를 통해 작동함
        1. place의 모든 예약 날짜의 퀴리셋을 받는다. (start_date, end_date를 이용하기 위함)
        2. 총 날짜를 계산한다. ex) start_date = 19.07.01, end_date = 19.07.05라면
        reserved_list = [190701, 190702, 190703, 190704, 190705] 가 저장 됨
        3. 그것을 place의 reserved_date에 제이슨으로 변경하여 스트링으로 저장한다.
        * why : 필드값에 배열로 저장 할 수 없기 때문에 str로 변경 한 것임
        """

        reserved_list = []
        for reserved in self.reserveds.all():
            reserved_days = (reserved.end_date - reserved.start_date).days + 1
            reserved_list.extend(
                [int((reserved.start_date + datetime.timedelta(days=i)).strftime('%y%m%d')) for i in
                 range(reserved_days)])
        self.reserved_dates = json.dumps(reserved_list)
        self.save()

    def reserved_list(self):
        """
        ReservedDates의 외래키 릴레이트 네임인 reserveds를 통해 작동함
        1. place의 모든 예약 날짜의 퀴리셋을 받는다. (start_date, end_date를 출력하기 위해서)
        2. 모든 쿼리셋을 검색하여 예약 리스트를 만든다.
        return: [[190701, 190705], ...]

        부킹이 완료되면 - >
        """

        reserved_date_list = []
        for reserved in self.reserveds.all():
            reserved_date_list.append(
                [int(reserved.start_date.strftime('%y%m%d')), int(reserved.end_date.strftime('%y%m%d'))])
        return json.dumps(reserved_date_list)


class ReservedDates(models.Model):

    start_date = models.DateField()
    end_date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reserveds')


class Booking(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, )
    reservation = models.ForeignKey(ReservedDates, on_delete=models.CASCADE, related_name='booking')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='booking')
    price = models.PositiveIntegerField(default=0)
    number_guest = models.PositiveIntegerField(default=0)
    nights = models.PositiveIntegerField(default=0)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.room.reserved_update()
        return super().save()


class RoomReview(models.Model):
    """장소에 대한 유저의 리뷰"""
    writer = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name='room_review')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='review')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='room_review')
    text = models.TextField(blank=True)

    active = models.BooleanField(default=True)

    rating_1 = models.SmallIntegerField()
    rating_2 = models.SmallIntegerField()
    total_rating = models.SmallIntegerField(blank=True)

    def save(self, *args, **kwargs):
        self.total_rating = round(((self.rating_1 + self.rating_2) / 2), 2)
        super(RoomReview, self).save()
        self.room.room_rating()


