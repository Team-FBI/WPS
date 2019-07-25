from django.urls import path
from .views import view_room

urlpatterns = [
    path('<slug:room_name>', view_room, name='room'),
]
