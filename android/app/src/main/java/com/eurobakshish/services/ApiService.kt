package com.eurobakshish.services

import com.eurobakshish.models.*
import retrofit2.Response
import retrofit2.http.*

/**
 * API interface for Euro Bakshish backend
 */
interface ApiService {
    
    // Authentication
    @POST("users/token/")
    suspend fun login(@Body credentials: LoginRequest): Response<TokenResponse>
    
    @POST("users/")
    suspend fun register(@Body userData: RegisterRequest): Response<User>
    
    @GET("users/me/")
    suspend fun getCurrentUser(): Response<User>
    
    // Trips
    @POST("trips/")
    suspend fun createTrip(@Body trip: TripCreateRequest): Response<Trip>
    
    @GET("trips/my_trips/")
    suspend fun getMyTrips(): Response<List<Trip>>
    
    @GET("trips/trip_history/")
    suspend fun getTripHistory(@Query("role") role: String): Response<List<Trip>>
    
    @POST("trips/{id}/accept/")
    suspend fun acceptTrip(@Path("id") tripId: Int): Response<Trip>
    
    @POST("trips/{id}/start/")
    suspend fun startTrip(@Path("id") tripId: Int): Response<Trip>
    
    @POST("trips/{id}/complete/")
    suspend fun completeTrip(@Path("id") tripId: Int): Response<Trip>
    
    @POST("trips/{id}/cancel/")
    suspend fun cancelTrip(@Path("id") tripId: Int): Response<Trip>
    
    // Reviews
    @POST("ratings/reviews/")
    suspend fun createReview(@Body review: ReviewCreateRequest): Response<Review>
    
    @GET("ratings/reviews/my_reviews_received/")
    suspend fun getMyReviewsReceived(): Response<List<Review>>
    
    @GET("ratings/reviews/my_reviews_given/")
    suspend fun getMyReviewsGiven(): Response<List<Review>>
    
    @GET("ratings/reviews/pending_reviews/")
    suspend fun getPendingReviews(): Response<List<PendingReview>>
}

// Request/Response models
data class LoginRequest(val username: String, val password: String)
data class TokenResponse(val access: String, val refresh: String)

data class RegisterRequest(
    val username: String,
    val email: String,
    val password: String,
    val password2: String,
    @SerializedName("first_name") val firstName: String,
    @SerializedName("last_name") val lastName: String,
    @SerializedName("phone_number") val phoneNumber: String?,
    @SerializedName("user_type") val userType: String
)

data class PendingReview(
    @SerializedName("trip_id") val tripId: Int,
    @SerializedName("trip_details") val tripDetails: TripDetails,
    @SerializedName("user_to_review") val userToReview: UserToReview
)

data class TripDetails(
    @SerializedName("start_location") val startLocation: String,
    @SerializedName("end_location") val endLocation: String,
    @SerializedName("completed_at") val completedAt: String
)

data class UserToReview(
    val id: Int,
    val username: String,
    @SerializedName("full_name") val fullName: String
)
