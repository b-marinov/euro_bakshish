package com.eurobakshish.models

import com.google.gson.annotations.SerializedName

/**
 * User model representing a user in the system
 */
data class User(
    val id: Int,
    val username: String,
    val email: String,
    @SerializedName("first_name")
    val firstName: String,
    @SerializedName("last_name")
    val lastName: String,
    @SerializedName("user_type")
    val userType: String,
    @SerializedName("phone_number")
    val phoneNumber: String?,
    @SerializedName("profile_picture")
    val profilePicture: String?,
    @SerializedName("date_of_birth")
    val dateOfBirth: String?,
    @SerializedName("passenger_profile")
    val passengerProfile: PassengerProfile?,
    @SerializedName("driver_profile")
    val driverProfile: DriverProfile?,
    @SerializedName("average_rating")
    val averageRating: Double?,
    @SerializedName("created_at")
    val createdAt: String,
    @SerializedName("updated_at")
    val updatedAt: String
)

data class PassengerProfile(
    val id: Int,
    @SerializedName("preferred_payment_method")
    val preferredPaymentMethod: String,
    @SerializedName("total_trips")
    val totalTrips: Int,
    @SerializedName("average_rating")
    val averageRating: Double?
)

data class DriverProfile(
    val id: Int,
    @SerializedName("license_number")
    val licenseNumber: String,
    @SerializedName("vehicle_make")
    val vehicleMake: String,
    @SerializedName("vehicle_model")
    val vehicleModel: String,
    @SerializedName("vehicle_year")
    val vehicleYear: Int,
    @SerializedName("vehicle_color")
    val vehicleColor: String,
    @SerializedName("vehicle_plate_number")
    val vehiclePlateNumber: String,
    @SerializedName("is_verified")
    val isVerified: Boolean,
    @SerializedName("is_available")
    val isAvailable: Boolean,
    @SerializedName("total_trips")
    val totalTrips: Int,
    @SerializedName("average_rating")
    val averageRating: Double?
)
