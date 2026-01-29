package com.eurobakshish.models

import com.google.gson.annotations.SerializedName

/**
 * Review model for rating system
 */
data class Review(
    val id: Int,
    val trip: Int,
    val reviewer: Int,
    @SerializedName("reviewed_user")
    val reviewedUser: Int,
    val rating: Int,
    val comment: String?,
    @SerializedName("punctuality_rating")
    val punctualityRating: Int?,
    @SerializedName("cleanliness_rating")
    val cleanlinessRating: Int?,
    @SerializedName("safety_rating")
    val safetyRating: Int?,
    @SerializedName("communication_rating")
    val communicationRating: Int?,
    @SerializedName("created_at")
    val createdAt: String
)

/**
 * Request model for creating a review
 */
data class ReviewCreateRequest(
    val trip: Int,
    @SerializedName("reviewed_user")
    val reviewedUser: Int,
    val rating: Int,
    val comment: String? = null,
    @SerializedName("punctuality_rating")
    val punctualityRating: Int? = null,
    @SerializedName("cleanliness_rating")
    val cleanlinessRating: Int? = null,
    @SerializedName("safety_rating")
    val safetyRating: Int? = null,
    @SerializedName("communication_rating")
    val communicationRating: Int? = null
)
