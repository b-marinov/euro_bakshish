"""
User models for the Euro Bakshish application.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Base model for all users in the system.
    """
    USER_TYPE_CHOICES = [
        ('passenger', 'Passenger'),
        ('driver', 'Driver'),
        ('both', 'Both'),
    ]
    
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='passenger'
    )
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.user_type})"
    
    @property
    def average_rating(self):
        """Calculate average rating across all roles."""
        ratings = []
        if hasattr(self, 'passenger_profile') and self.passenger_profile:
            ratings.append(self.passenger_profile.average_rating)
        if hasattr(self, 'driver_profile') and self.driver_profile:
            ratings.append(self.driver_profile.average_rating)
        
        valid_ratings = [r for r in ratings if r is not None]
        if valid_ratings:
            return sum(valid_ratings) / len(valid_ratings)
        return None


class PassengerProfile(models.Model):
    """
    Profile for passengers.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='passenger_profile'
    )
    preferred_payment_method = models.CharField(
        max_length=50,
        default='cash',
        choices=[
            ('cash', 'Cash'),
            ('card', 'Card'),
            ('digital_wallet', 'Digital Wallet'),
        ]
    )
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    total_trips = models.IntegerField(default=0)
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Passenger: {self.user.username}"
    
    def update_rating(self):
        """Update average rating based on all reviews."""
        from apps.ratings.models import Review
        reviews = Review.objects.filter(
            reviewed_user=self.user,
            trip__passenger=self.user
        )
        if reviews.exists():
            self.average_rating = reviews.aggregate(
                models.Avg('rating')
            )['rating__avg']
            self.save()


class DriverProfile(models.Model):
    """
    Profile for drivers.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='driver_profile'
    )
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry = models.DateField()
    vehicle_make = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    vehicle_year = models.IntegerField()
    vehicle_color = models.CharField(max_length=30)
    vehicle_plate_number = models.CharField(max_length=20, unique=True)
    vehicle_capacity = models.IntegerField(default=4)
    insurance_number = models.CharField(max_length=50)
    insurance_expiry = models.DateField()
    is_verified = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)
    total_trips = models.IntegerField(default=0)
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Driver: {self.user.username} - {self.vehicle_make} {self.vehicle_model}"
    
    def update_rating(self):
        """Update average rating based on all reviews."""
        from apps.ratings.models import Review
        reviews = Review.objects.filter(
            reviewed_user=self.user,
            trip__driver=self.user
        )
        if reviews.exists():
            self.average_rating = reviews.aggregate(
                models.Avg('rating')
            )['rating__avg']
            self.save()
