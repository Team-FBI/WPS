from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<slug:room_name>/', ChatConsumer),
]
