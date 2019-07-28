from locations.models import Country, State
from rest_framework import serializers
from reservations.models import RoomReservation

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name"]


class StateSerializer(serializers.ModelSerializer):
    rooms = serializers.SerializerMethodField()
    reservations = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()

    def get_country(self, object):
        return object.country.name

    def get_rooms(self, object):
        return object.rooms.count()

    def get_reservations(self, object):
        return RoomReservation.objects.filter(room__state__name=object.name).count()

    class Meta:
        model = State
        fields = ["name", "country", "rooms", "reservations"]