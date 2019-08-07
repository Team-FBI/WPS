from django.urls import path
from .views import WishListListAPIView, WishListRetrieveUpdateAPIView, \
    WishListIsSavedListAPIView, add_or_remove_room_in_wish_list

urlpatterns = [
    path('', WishListListAPIView.as_view()),
    path('<int:pk>/', WishListRetrieveUpdateAPIView.as_view()),
    path('list/room/<int:room_id>/', WishListIsSavedListAPIView.as_view()),
    path('<int:wish_list_id>/save/room/<int:room_id>/', add_or_remove_room_in_wish_list),
]
