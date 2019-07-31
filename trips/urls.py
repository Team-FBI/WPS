from django.urls import path
from .views import *

urlpatterns = [
    path("trip-category/", TripCategoryList.as_view(), name=TripCategoryList.name),
    path("trip-category/<int:pk>/", TripCategoryDetail.as_view(), name=TripCategoryDetail.name),
    path("/", TripList.as_view(), name=TripList.name),
    path("<int:pk>/", TripDetail.as_view(), name=TripDetail.name),
    path("reservation/", TripReservationCreate.as_view(), name=TripReservationCreate.name),
    path("review/", TripReviewCreate.as_view(), name=TripReviewCreate.name),
    path("state/", StateList.as_view(), name=StateList.name),
    path("state/<int:pk>/", StateDetail.as_view(), name=StateDetail.name),


]
