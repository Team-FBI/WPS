from django.urls import include, path
from rest_framework import routers
from rooms import views
from reservations.views import ReservationCreateView

app_name = "rooms"
urlpatterns = [
    path("", views.RoomListView.as_view()),
    path("create/", views.RoomCreateView.as_view()),
    path("<int:pk>", ReservationCreateView.as_view()),
    path("<int:pk>/", views.RoomDetailView.as_view()),
    path("update/<int:pk>/", views.RoomUpdateView.as_view()),
    path("like/", views.RoomLikeListView.as_view()),
    path("like/<int:pk>/", views.RoomLikeCreateView.as_view()),
    path("like/<int:pk>", views.RoomLikeDestroyView.as_view()),
]
