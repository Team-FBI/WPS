from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from locations.models import State
import uuid


def n_tuple(n, first=[], last=[]):
    return tuple(first + [(i, i) for i in range(1, n)] + last)


ROOM_TYPES = [
    (1, "Apartment"),
    (2, "House"),
    (3, "Garden House"),
    (4, "Bed and Breakfast"),
    (5, "Villa"),
    (6, "Caravan"),
    (7, "Office"),
]

SPACE_TYPES = [(1, "Entire room"), (2, "Private Room"), (3, "Shared Room")]

BATHROOM_TYPES = [(1, "Private"), (2, "Shared")]

CANCELATION_RULES = [(1, "Flexible"), (2, "Semi-flexible"), (3, "Strict")]


def get_upload_path(instance, filename):
    if isinstance(instance, Facility):
        ends = filename.split(".")[-1]
        path = f"facilities/{instance.name}.{ends}"
    else:
        path = f"rooms/{instance.host.id}/{instance.slug}/{filename}"
    return path


class Facility(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to=get_upload_path, blank=True, null=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="rooms"
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    address = models.CharField(max_length=250, blank=True)
    state = models.ForeignKey(
        State, on_delete=models.SET_NULL, related_name="rooms", null=True, blank=False
    )
    postal_code = models.CharField(max_length=15, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    check_in = models.TimeField(blank=True, null=True, default=)
    check_out = models.TimeField(blank=True, null=True)
    image = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    image_1 = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    image_2 = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    image_3 = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    image_4 = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    image_5 = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    image_6 = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    bed_image_0 = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    bed_image_1 = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    bed_image_2 = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    bed_image_3 = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    bed_image_4 = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    bed_image_5 = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, null=True)
    room_type = models.SmallIntegerField(choices=ROOM_TYPES, default=1)
    space = models.SmallIntegerField(choices=SPACE_TYPES, default=1)
    capacity = models.PositiveSmallIntegerField(default=1)
    bedroom = models.PositiveSmallIntegerField(default=1)
    beds = models.PositiveSmallIntegerField(default=1)
    bathroom = models.PositiveSmallIntegerField(default=0)
    min_stay = models.PositiveSmallIntegerField(default=1)
    max_stay = models.PositiveSmallIntegerField(default=10)
    bath_type = models.SmallIntegerField(choices=BATHROOM_TYPES, default=1)
    cancellation = models.SmallIntegerField(choices=CANCELATION_RULES, default=1)
    description = models.TextField(blank=True, null=True)
    locational_description = models.TextField(blank=True, null=True)
    total_rating = models.FloatField(default=0)
    accuracy_score = models.FloatField(default=0)
    location_score = models.FloatField(default=0)
    communication_score = models.FloatField(default=0)
    checkin_score = models.FloatField(default=0)
    clean_score = models.FloatField(default=0)
    value_score = models.FloatField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    facilities = models.ManyToManyField(Facility, related_name="rooms")

    class Meta:
        ordering = ["-created_at", "-updated_at"]

    def save(self):
        self.slug = slugify(self.title)
        return super().save()

    def __str__(self):
        return f"{self.state.name} / {self.slug} / {self.host}"

