from django.db.models import Q
from rest_framework import filters
from reservations.views import reservation_validation


class CapacityFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        capacity = request.query_params.get("capacity", None)
        if capacity:
            queryset = queryset.filter(capacity__gte=capacity)
        return queryset

class DateFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        start_date = request.query_params.get("start_date", None)
        end_date = request.query_params.get("end_date", None)
        if start_date and end_date:
            queryset = reservation_validation(queryset, start_date, end_date)
        return queryset


class PriceFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        min_price = request.query_params.get("min_price", 0)
        max_price = request.query_params.get("max_price", None)
        condition_min = Q(price__gte=min_price)
        if not max_price:
            return queryset.filter(condition_min)
        condition_max = Q(price__lte=max_price)
        return queryset.filter(condition_min & condition_max)

class RatingFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        rating = request.query_params.get("rating", None)
        if rating:
            return queryset.filter(Q(total_rating__gte=int(rating)))
        return queryset