from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('custom_display_name', 'email', 'is_coordinator', 'is_planner', 'is_staff', 'is_superuser')
    list_filter = ('is_coordinator', 'is_planner', 'is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Roles', {'fields': ('is_coordinator', 'is_planner')}),
    )

    def custom_display_name(self, obj):
        return f"{obj.first_name} {obj.last_name}" if obj.first_name else obj.username

    custom_display_name.short_description = "Full Name"

# Change model name in admin panel
CustomUser._meta.verbose_name = "Member"
CustomUser._meta.verbose_name_plural = "Members"

admin.site.register(CustomUser, CustomUserAdmin)

# Customize admin panel branding
admin.site.site_header = "My Custom Admin Panel"
admin.site.site_title = "Admin Dashboard"
admin.site.index_title = "Welcome to the Admin Panel"
