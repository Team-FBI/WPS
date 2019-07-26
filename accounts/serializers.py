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
        raise_errors_on_nested_writes("update", self, validated_data)
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.set_password(instance.password)
        instance.save()
        return instance


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
            "is_staff",
        ]

    def create(self, validated_data):
        key_a = "FBI_I"
        key_b = "FBI_F"
        if all(
            [
                key_a not in validated_data["username"],
                key_b not in validated_data["username"],
            ]
        ):
            raise PermissionError("not registered id for staff", "dont do it")
        print(validated_data)
        validated_data["is_staff"] = True
        return self.Meta.model.objects.create_user(**validated_data)


class AdminSerializer(StaffSerializer):
    def create(self, validated_data):
        if "FBI_B" not in validated_data["username"]:
            raise PermissionError("not registered email", "never do it")
        return self.Meta.model.objects.create_superuser(**validated_data)
