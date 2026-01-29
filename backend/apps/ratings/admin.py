"""
Admin configuration for ratings app
"""
from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'trip', 'reviewer', 'reviewed_user',
        'rating', 'created_at'
    ]
    list_filter = ['rating', 'created_at']
    search_fields = [
        'reviewer__username', 'reviewed_user__username',
        'comment'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Trip & Users', {
            'fields': ('trip', 'reviewer', 'reviewed_user')
        }),
        ('Rating', {
            'fields': ('rating', 'comment')
        }),
        ('Detailed Ratings', {
            'fields': (
                'punctuality_rating', 'cleanliness_rating',
                'safety_rating', 'communication_rating'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
