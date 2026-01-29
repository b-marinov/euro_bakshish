package com.eurobakshish.models

import com.google.gson.annotations.SerializedName

/**
 * Trip model representing a ride/trip
 */
data class Trip(
    val id: Int,
    val passenger: Int,
    val driver: Int?,
    @SerializedName("start_location_name")
    val startLocationName: String,
    @SerializedName("start_latitude")
    val startLatitude: Double,
    @SerializedName("start_longitude")
    val startLongitude: Double,
    @SerializedName("end_location_name")
    val endLocationName: String,
    @SerializedName("end_latitude")
    val endLatitude: Double,
    @SerializedName("end_longitude")
    val endLongitude: Double,
    val status: String,
    @SerializedName("distance_km")
    val distanceKm: Double?,
    @SerializedName("estimated_duration_minutes")
    val estimatedDurationMinutes: Int?,
    val fare: Double?,
    @SerializedName("requested_at")
    val requestedAt: String,
    @SerializedName("completed_at")
    val completedAt: String?,
    @SerializedName("passenger_notes")
    val passengerNotes: String?,
    @SerializedName("number_of_passengers")
    val numberOfPassengers: Int
)

/**
 * Request model for creating a trip
 */
data class TripCreateRequest(
    @SerializedName("start_location_name")
    val startLocationName: String,
    @SerializedName("start_latitude")
    val startLatitude: Double,
    @SerializedName("start_longitude")
    val startLongitude: Double,
    @SerializedName("end_location_name")
    val endLocationName: String,
    @SerializedName("end_latitude")
    val endLatitude: Double,
    @SerializedName("end_longitude")
    val endLongitude: Double,
    @SerializedName("passenger_notes")
    val passengerNotes: String? = null,
    @SerializedName("number_of_passengers")
    val numberOfPassengers: Int = 1
)
