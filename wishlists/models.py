from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db import models
from rooms.models import Room

User = get_user_model()


class WishList(models.Model):
    title = models.CharField(max_length=30)
    is_public = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wish_lists')
    rooms = models.ManyToManyField(Room, null=True, blank=True)
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    adult = models.PositiveSmallIntegerField(default=1)
    kid = models.PositiveSmallIntegerField(default=0)
    infant = models.PositiveSmallIntegerField(default=0)

    @property
    def rooms_number(self):
        return self.rooms.count()

    @property
    def guest_number(self):
        return self.adult + self.kid

    @property
    def image(self):
        if not self.rooms.exists():
            return
        return self.rooms.last().image.url

    @property
    def rooms_valid(self):
        if self.check_in is None and self.check_out is None:
            return self.rooms
        stay = (self.check_out - self.check_in).days
        rooms = self.rooms.prefetch_related('reservations').filter(capacity__gte=self.guest_number, min_stay__lte=stay,
                                                                   max_stay__gte=stay)
        check_in_q = Q(start_date__lte=self.check_in, end_date__gt=self.check_in)
        check_out_q = Q(start_date__lt=self.check_out, end_date__gte=self.check_out)
        excludes = set()
        for room in rooms:
            if not room.reservations.exists():
                continue
            is_invalid = room.reservations.filter(check_in_q | check_out_q).exists()
            if is_invalid:
                excludes.add(room.id)
        return rooms.exclude(id__in=excludes)
