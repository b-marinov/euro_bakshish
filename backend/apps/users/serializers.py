"""
Serializers for User models
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, PassengerProfile, DriverProfile


class PassengerProfileSerializer(serializers.ModelSerializer):
    """Serializer for PassengerProfile"""
    
    class Meta:
        model = PassengerProfile
        fields = [
            'id', 'preferred_payment_method', 'emergency_contact_name',
            'emergency_contact_phone', 'total_trips', 'average_rating',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_trips', 'average_rating', 'created_at', 'updated_at']


class DriverProfileSerializer(serializers.ModelSerializer):
    """Serializer for DriverProfile"""
    
    class Meta:
        model = DriverProfile
        fields = [
            'id', 'license_number', 'license_expiry', 'vehicle_make',
            'vehicle_model', 'vehicle_year', 'vehicle_color',
            'vehicle_plate_number', 'vehicle_capacity', 'insurance_number',
            'insurance_expiry', 'is_verified', 'is_available', 'total_trips',
            'average_rating', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_verified', 'total_trips', 'average_rating', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    passenger_profile = PassengerProfileSerializer(read_only=True)
    driver_profile = DriverProfileSerializer(read_only=True)
    average_rating = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'phone_number', 'profile_picture', 'date_of_birth',
            'passenger_profile', 'driver_profile', 'average_rating',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    passenger_profile = PassengerProfileSerializer(required=False)
    driver_profile = DriverProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = [
            'username', 'password', 'password2', 'email', 'first_name',
            'last_name', 'user_type', 'phone_number', 'date_of_birth',
            'passenger_profile', 'driver_profile'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Validate that appropriate profile data is provided
        user_type = attrs.get('user_type')
        if user_type in ['passenger', 'both'] and 'passenger_profile' not in attrs:
            attrs['passenger_profile'] = {}
        if user_type in ['driver', 'both'] and 'driver_profile' not in attrs:
            raise serializers.ValidationError({"driver_profile": "Driver profile is required for driver accounts."})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        passenger_data = validated_data.pop('passenger_profile', None)
        driver_data = validated_data.pop('driver_profile', None)
        
        user = User.objects.create_user(**validated_data)
        
        # Create profiles based on user type
        if user.user_type in ['passenger', 'both'] and passenger_data is not None:
            PassengerProfile.objects.create(user=user, **passenger_data)
        
        if user.user_type in ['driver', 'both'] and driver_data is not None:
            DriverProfile.objects.create(user=user, **driver_data)
        
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user information"""
    
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'phone_number',
            'profile_picture', 'date_of_birth'
        ]
