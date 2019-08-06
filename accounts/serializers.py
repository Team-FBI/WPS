from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.utils import model_meta
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.exceptions import ErrorDetail, ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from config.utils import response_error_handler


@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "image", "description"]


class UserDetailSerializer(serializers.ModelSerializer):
    reservations = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "image",
            "description",
            "rooms",
            "reservations",
            "likes",
        ]

    def get_reservations(self, obj):
        reservations = obj.reservations.all()
        return [
            {
                f"{r.room.state.name}-{r.id}": {
                    "start_date": r.start_date,
                    "end_date": r.end_date,
                    "room": r.room.id,
                    "id": r.id,
                    "title": r.room.title,
                    "image": r.room.image.url
                }
            }
            for r in reservations
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "image",
            "description",
        ]

    def create(self, validated_data):
        instance = self.Meta.model.objects.create_user(**validated_data)
        return instance

    def update(self, instance, validated_data):
        instance.set_password(instance.password)
        return super().update(instance, validated_data)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "password",
            "image",
            "description",
        ]

    def create(self, validated_data):
        validated_data["is_staff"] = True
        return self.Meta.model.objects.create_user(**validated_data)


class AdminSerializer(StaffSerializer):
    def create(self, validated_data):
        return self.Meta.model.objects.create_superuser(**validated_data)
