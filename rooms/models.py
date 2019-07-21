from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from locations.models import State


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


class Facility(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="rooms"
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    address = models.CharField(max_length=250, blank=True)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING, related_name="rooms")
    postal_code = models.CharField(max_length=15, blank=False, null=True)
    mobile = models.CharField(max_length=30, blank=False, null=False)
    image = models.ImageField(upload_to=f"rooms/%Y/%m/%d/", blank=False, null=True)
    image_1 = models.ImageField(upload_to=f"rooms/%Y/%m/%d/", blank=True, null=True)
    image_2 = models.ImageField(upload_to=f"rooms/%Y/%m/%d/", blank=True, null=True)
    image_3 = models.ImageField(upload_to=f"rooms/%Y/%m/%d/", blank=True, null=True)
    image_4 = models.ImageField(upload_to=f"rooms/%Y/%m/%d/", blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, null=True)
    capacity = models.SmallIntegerField(choices=NO_OF_BEDS, default=6)
    room_type = models.SmallIntegerField(choices=ROOM_TYPES, default=1)
    space = models.SmallIntegerField(choices=SPACE_TYPES, default=1)
    bedroom = models.SmallIntegerField(choices=NO_OF_ROOMS, default=1)
    bath_type = models.SmallIntegerField(choices=BATHROOM_TYPES, default=1)
    bathroom = models.SmallIntegerField(choices=NO_OF_ROOMS, default=1)
    cancellation = models.SmallIntegerField(choices=CANCELATION_RULES, default=1)
    min_stay = models.SmallIntegerField(choices=MIN_STAY, default=1)
    max_stay = models.SmallIntegerField(choices=MAX_STAY, default=0)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_rating = models.FloatField(default=0)
    facilities = models.ManyToManyField(Facility, related_name="rooms")

    class Meta:
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        return f"{self.state.name} / {self.slug} / {self.host}"


class Reservation(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="reservations"
    )
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="reservations"
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def is_valid_date(self):
        Q_start_date = Q(start_date__lt=self.end_date)
        Q_end_date = Q(end_date__gt=self.start_date)

        if self.room.reservations.filter(~Q_start_date & ~Q_end_date).exists():
            return False
        return True


class Review(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, related_name="reviews"
    )
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reviews")
    description = models.TextField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    accuracy_score = models.FloatField(default=0)
    location_score = models.FloatField(default=0)
    communication_score = models.FloatField(default=0)
    checkin_score = models.FloatField(default=0)
    clean_score = models.FloatField(default=0)
    value_score = models.FloatField(default=0)
    total_score = models.FloatField(default=0)

    def save(self):
        rating_sum = (
            self.accuracy_score
            + self.location_score
            + self.communication_score
            + self.checkin_score
            + self.clean_score
            + self.value_score
        )
        total_score = rating_sum / 6
        self.total_score = round(total_score, 2)
        return super(Review, self).save()
