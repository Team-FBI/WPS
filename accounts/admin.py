from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class CustomUserAdmin(UserAdmin):
    UserAdmin.fieldsets[1][1]["fields"] += ("image", "description")
    UserAdmin.add_fieldsets += (
        (("Additional Info"), {"fields": ("image", "description")}),
    )


admin.site.register(get_user_model(), CustomUserAdmin)
