from django.urls import include, path
from rest_framework import routers
from rooms.views import RoomCreateView, RoomDetailView, RoomListView, RoomUpdateView, ReservationCreateView

app_name = "rooms"
urlpatterns = [
    path("", RoomListView.as_view()),
    path("create/", RoomCreateView.as_view()),
    path("<int:pk>/", RoomDetailView.as_view()),
    path("update/<int:pk>/", RoomUpdateView.as_view()),
    path("<int:pk>/reservation/", ReservationCreateView.as_view()),
]
