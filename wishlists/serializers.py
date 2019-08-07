from rest_framework import serializers
from rooms.serializers import RoomListSerializer
from .models import WishList


class WishListSerializer(serializers.ModelSerializer):
    rooms_valid = serializers.SerializerMethodField()
    rooms_invalid = serializers.SerializerMethodField()

    class Meta:
        model = WishList
        fields = (
            'title', 'check_in', 'check_out', 'adult', 'kid', 'infant', 'guest_number', 'is_public', 'rooms_valid',
            'rooms_invalid')

    def get_rooms_valid(self, obj):
        rooms_valid = obj.rooms_valid
        request = self.context.get("request")
        return RoomListSerializer(rooms_valid, many=True, context={'request': request}).data

    def get_rooms_invalid(self, obj):
        rooms_invalid = obj.rooms.exclude(id__in=obj.rooms_valid.all())
        request = self.context.get("request")
        return RoomListSerializer(rooms_invalid, many=True, context={'request': request}).data


class WishListListCreateSerializer(serializers.ModelSerializer):
    is_public = serializers.BooleanField(write_only=True)

    class Meta:
        model = WishList
        fields = ('id', 'title', 'is_public', 'image', 'rooms_number', 'guest_number')

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data["author"] = user
        return super().create(validated_data)


class WishListSaveListSerializer(serializers.ModelSerializer):
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = WishList
        fields = ('id', 'title', 'rooms_number', 'guest_number', 'is_saved')

    # TODO:check
    def get_is_saved(self, obj):
        room_id = self.context.get('view').kwargs.get('room_id')
        return obj.rooms.filter(pk=room_id).exists()
