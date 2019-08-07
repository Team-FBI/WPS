from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import WishList
from .serializers import (WishListSerializer, WishListSaveListSerializer,
                          WishListListCreateSerializer)

REMOVED_SUCCESSFULLY = "Removed successfully"
ADDED_SUCCESSFULLY = "Added successfully"
ERROR_UNAUTHENTICATED_USER = "User is not author of this wish list"


class WishListRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        wish_list = self.get_object()
        if wish_list.author != request.user:
            return Response({'detail': ERROR_UNAUTHENTICATED_USER}, status=status.HTTP_401_UNAUTHORIZED)
        return self.destroy(request, *args, **kwargs)


class WishListListAPIView(generics.ListCreateAPIView):
    queryset = WishList.objects.all()
    serializer_class = WishListListCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)


class WishListIsSavedListAPIView(generics.ListAPIView):
    queryset = WishList.objects.all()
    serializer_class = WishListSaveListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)


@api_view(http_method_names=['GET'])
@permission_classes((IsAuthenticated,))
def add_or_remove_room_in_wish_list(request, wish_list_id, room_id):
    wish_list = WishList.objects.get(pk=wish_list_id)
    if wish_list.author != request.user:
        return Response({'detail': ERROR_UNAUTHENTICATED_USER}, status=status.HTTP_401_UNAUTHORIZED)

    if wish_list.rooms.filter(pk=room_id).exists():
        wish_list.rooms.remove(room_id)
        message = REMOVED_SUCCESSFULLY
    else:
        wish_list.rooms.add(room_id)
        message = ADDED_SUCCESSFULLY
    return Response({'message': message}, status=status.HTTP_200_OK)
