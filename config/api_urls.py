from accounts.urls import urlpatterns as accounts_router
from locations.urls import urlpatterns as locations_router
from rooms.urls import urlpatterns as rooms_router
from reservations.urls import urlpatterns as reservations_router
from django.urls import include, path

urlpatterns = [
    path("accounts/", include(accounts_router), name="accounts"),
    path("rooms/", include(rooms_router), name="rooms"),
    path("locations/", include(locations_router), name="locations"),
    path("reservations/", include(reservations_router), name="reservations"),
]
