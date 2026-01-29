"""
Admin configuration for users app
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PassengerProfile, DriverProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'user_type', 'is_staff', 'created_at']
    list_filter = ['user_type', 'is_staff', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'profile_picture', 'date_of_birth')
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'date_of_birth')
        }),
    )


@admin.register(PassengerProfile)
class PassengerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_trips', 'average_rating', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email']


@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'vehicle_make', 'vehicle_model', 'vehicle_plate_number',
        'is_verified', 'is_available', 'total_trips', 'average_rating'
    ]
    list_filter = ['is_verified', 'is_available', 'created_at']
    search_fields = ['user__username', 'license_number', 'vehicle_plate_number']
    actions = ['verify_drivers', 'unverify_drivers']
    
    def verify_drivers(self, request, queryset):
        queryset.update(is_verified=True)
    verify_drivers.short_description = "Verify selected drivers"
    
    def unverify_drivers(self, request, queryset):
        queryset.update(is_verified=False)
    unverify_drivers.short_description = "Unverify selected drivers"
