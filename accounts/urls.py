from django.urls import include, path
from rest_framework import routers
from accounts import views
from rest_framework.authtoken import views as auth_views
from accounts.f_views import get_user_view
app_name = "accounts"

urlpatterns = [
    path("user/", views.UserListView.as_view()),
    path("user/<int:pk>/", views.UserDetailView.as_view()),
    path("staff/", views.StaffListCreateView.as_view()),
    path("admin/", views.AdminListCreateView.as_view()),
    path("get_token/", auth_views.obtain_auth_token),
]