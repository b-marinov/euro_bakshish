"""
Admin configuration for trips app
"""
from django.contrib import admin
from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'passenger', 'driver', 'start_location_name',
        'end_location_name', 'status', 'fare', 'requested_at'
    ]
    list_filter = ['status', 'requested_at', 'completed_at']
    search_fields = [
        'passenger__username', 'driver__username',
        'start_location_name', 'end_location_name'
    ]
    readonly_fields = ['requested_at', 'accepted_at', 'started_at', 'completed_at', 'cancelled_at']
    
    fieldsets = (
        ('Participants', {
            'fields': ('passenger', 'driver')
        }),
        ('Locations', {
            'fields': (
                'start_location_name', 'start_latitude', 'start_longitude',
                'end_location_name', 'end_latitude', 'end_longitude'
            )
        }),
        ('Trip Details', {
            'fields': (
                'status', 'distance_km', 'estimated_duration_minutes',
                'fare', 'number_of_passengers'
            )
        }),
        ('Timestamps', {
            'fields': (
                'requested_at', 'accepted_at', 'started_at',
                'completed_at', 'cancelled_at'
            )
        }),
        ('Notes', {
            'fields': ('passenger_notes', 'driver_notes')
        }),
    )
