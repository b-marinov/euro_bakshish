"""
Tests for User models
"""
import pytest
from django.contrib.auth import get_user_model
from apps.users.models import PassengerProfile, DriverProfile

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Test User model"""
    
    def test_create_user(self):
        """Test creating a basic user"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            user_type='passenger'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.user_type == 'passenger'
    
    def test_create_passenger_profile(self):
        """Test creating a passenger profile"""
        user = User.objects.create_user(
            username='passenger1',
            email='passenger@example.com',
            password='testpass123',
            user_type='passenger'
        )
        profile = PassengerProfile.objects.create(
            user=user,
            preferred_payment_method='card'
        )
        assert profile.user == user
        assert profile.total_trips == 0
        assert profile.average_rating is None
    
    def test_create_driver_profile(self):
        """Test creating a driver profile"""
        user = User.objects.create_user(
            username='driver1',
            email='driver@example.com',
            password='testpass123',
            user_type='driver'
        )
        profile = DriverProfile.objects.create(
            user=user,
            license_number='DL12345',
            license_expiry='2025-12-31',
            vehicle_make='Toyota',
            vehicle_model='Camry',
            vehicle_year=2020,
            vehicle_color='Silver',
            vehicle_plate_number='ABC123',
            insurance_number='INS12345',
            insurance_expiry='2025-12-31'
        )
        assert profile.user == user
        assert profile.vehicle_make == 'Toyota'
        assert profile.is_verified is False
        assert profile.total_trips == 0
