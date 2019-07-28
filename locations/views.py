from rest_framework import viewsets, filters
from locations.models import Country, State
from locations.serializers import CountrySerializer, StateSerializer


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    filter_backends = [
        filters.SearchFilter
    ]
    search_fields = ["^name"]


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
