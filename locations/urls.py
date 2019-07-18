from django.urls import include, path
from rest_framework import routers
from locations import views

locations_router = routers.DefaultRouter()
locations_router.register("country", views.CountryViewSet)
locations_router.register("state", views.StateViewSet)
app_name = "locations"

urlpatterns = [path("", include(locations_router.urls))]
