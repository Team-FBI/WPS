from django.contrib import admin
from django.urls import path, include
from chat.views import view_room
from django.contrib.auth import urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-doc/", include("config.yasg_urls")),
    path("api/", include("config.api_urls")),
    # path("accounts/", include("rest_framework.urls")),
    path("api-auth/", include('rest_framework.urls')),
    path("chat-test/<int:reservation_id>/", view_room)
]
