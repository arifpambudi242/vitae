from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Response


# Register your models here.
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Address', {
            'fields': ('address_1', 'address_2', 'suburb', 'postcode', 'state', 'country', 'phone'),
        }),
    )


@admin.register(User)
class UserAdmin(CustomUserAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'username', 'is_staff')
    list_display_links = ('id', 'first_name', 'last_name', 'email', 'username')


admin.site.register(Response)