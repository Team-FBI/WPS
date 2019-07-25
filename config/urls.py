from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-doc/", include("config.yasg_urls")),
    path("api/", include("config.api_urls")),
    # path("accounts/", include("rest_framework.urls")),
    path("api-auth/", include('rest_framework.urls')),
    path('chat/', include('chat.urls'))  # TODO: remove when test ends
]
