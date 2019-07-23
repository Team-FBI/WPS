from django.urls import include, path
from reservations.views import ReservationDetailUpdateView

app_name = "reservations"
urlpatterns = [path("rooms/<int:pk>/", ReservationDetailUpdateView.as_view())]
