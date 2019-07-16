from django.urls import path, include
from rest_framework.permissions import (
    IsAdminUser,
    AllowAny,
    IsAuthenticated,
    DjangoModelPermissionsOrAnonReadOnly,
)
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from config.api_urls import urlpatterns
from rest_framework.authentication import SessionAuthentication
# default open api
base_patterns = [path("api/", include(urlpatterns))]

from django.contrib.auth.context_processors import auth

# 내부 개발자용
schema_url_admin_patterns = base_patterns
schema_view_admin = get_schema_view(
    openapi.Info(
        title="내부 개발자용 API Documentation",
        description="내부 개발자용 API문서 페이지",
        default_version="v1",
        terms_of_service="https://oh-mon-lesiles.shop/policies/terms/",
        contact=openapi.Contact(email="charlesjune@daum.net"),
        license=openapi.License(name="junehan python"),
    ),
    validators=["flex"],
    public=False,
    permission_classes=(IsAdminUser,),
    patterns=schema_url_admin_patterns,
)

# 외부 사용자용
schema_url_public_patterns = base_patterns + [
    # path(),
]

schema_view_public = get_schema_view(
    openapi.Info(
        title="외부 자원용 API Documentation",
        default_version="v2",
        description="외부자원에서 사용할 수 있는 페이지입니다.",
        terms_of_service="https://oh-mon-lesiles.shop/policies/terms/",
        contact=openapi.Contact(email="charlesjune@daum.net"),
        license=openapi.License(name="junehan python"),
    ),
    validators=["flex"],
    public=True,
    permission_classes=(
        AllowAny,
    ),
    patterns=schema_url_public_patterns,
)
app_name = "api"
urlpatterns = [
    path("admin/", schema_view_admin.with_ui(), name="admin"),
    path("staff/", schema_view_public.with_ui(), name="staff"),
    path("no_view/", schema_view_public.without_ui(), name='no_ui'),
]
