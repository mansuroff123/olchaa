from django.contrib import admin
from .models import UserModel


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "admin_image", "username", "first_name", "last_name", "phone", "email",)
    list_display_links = ('id', 'username', 'first_name', 'last_name')
    list_filter = ("date_joined",)
    search_fields = ("username", "phone")
