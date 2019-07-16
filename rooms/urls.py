from django.urls import include, path
from rest_framework import routers
from rooms import views
app_name = "rooms"
urlpatterns = [
    path("", views.RoomListView.as_view()),
    path("create/", views.RoomCreateView.as_view()),
    path("<int:pk>/", views.RoomDetailView.as_view()),
    path("update/<int:pk>/", views.RoomUpdateView.as_view()),
    path("<int:pk>/booking/", views.BookingCreateAPI.as_view()),
]
