from django.urls import path
from .views import *

urlpatterns = [
    path("main/", TripMain.as_view(), name=TripMain.name),
    path("category/", TripCategoryList.as_view(), name=TripCategoryList.name),
    path("category/<int:pk>/", TripCategoryDetail.as_view(), name=TripCategoryDetail.name),
    path("trips", TripList.as_view(), name=TripList.name),
    path("trips/schedule/", TripScheduleList.as_view(), name=TripScheduleList.name),
    path("trips/<int:pk>/", TripDetail.as_view(), name=TripDetail.name),
    path("reservation/", TripReservationCreate.as_view(), name=TripReservationCreate.name),
    path("reservation/<int:pk>/", TripReservationDetail.as_view(), name=TripReservationDetail.name),
    path("review/", TripReviewCreate.as_view(), name=TripReviewCreate.name),
    path("state/", StateList.as_view(), name=StateList.name),
    path("state/<int:pk>/", StateDetail.as_view(), name=StateDetail.name),
    path("", ApiRoot.as_view(), name=ApiRoot.name),

]
