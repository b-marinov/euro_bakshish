# Euro Bakshish API Documentation

## Overview

The Euro Bakshish API is a RESTful API for a ride-sharing application that connects passengers with drivers. The API supports user registration, trip management, and rating systems.

## Base URL
`http://localhost:8000/api/`

## Interactive API Documentation

The API provides interactive documentation powered by Swagger UI:

- **Swagger UI**: `http://localhost:8000/api/docs/` - Interactive API explorer with try-it-out functionality
- **OpenAPI Schema**: `http://localhost:8000/api/schema/` - Machine-readable API specification

## Authentication

All endpoints except registration and login require JWT (JSON Web Token) authentication.

### Getting Started
1. Register a new user account
2. Obtain JWT tokens using your credentials
3. Include the access token in all subsequent requests

### Token Usage
Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

### Token Refresh
Access tokens expire after 60 minutes by default. Use the refresh token to obtain a new access token without re-authenticating:
```
POST /api/users/token/refresh/
Body: {"refresh": "your-refresh-token"}
```

## Endpoints

### API Root
```
GET /api/
Response: {
  "message": "Euro Bakshish API",
  "version": "1.0",
  "endpoints": {
    "users": "/api/users/",
    "trips": "/api/trips/",
    "ratings": "/api/ratings/",
    "docs": "/api/docs/",
    "schema": "/api/schema/"
  }
}
```

### Authentication

#### Register User
Create a new user account. No authentication required.

```
POST /api/users/
Body: {
  "username": "string",
  "email": "string",
  "password": "string",
  "password2": "string",  // Must match password
  "first_name": "string",
  "last_name": "string",
  "phone_number": "string",
  "user_type": "passenger|driver|both"  // Choose one
}
Response: {
  "id": number,
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "phone_number": "string",
  "user_type": "string",
  "created_at": "datetime"
}
```

#### Login (Obtain Token)
Authenticate and receive JWT tokens.

```
POST /api/users/token/
Body: {
  "username": "string",
  "password": "string"
}
Response: {
  "access": "string",   // Access token (expires in 60 minutes)
  "refresh": "string"   // Refresh token (expires in 24 hours)
}
```

#### Refresh Token
Get a new access token using refresh token.

```
POST /api/users/token/refresh/
Body: {
  "refresh": "string"
}
Response: {
  "access": "string",
  "refresh": "string"  // New refresh token if rotation enabled
}
```

#### Get Current User
Get authenticated user's profile.

```
GET /api/users/me/
Response: {
  "id": number,
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "phone_number": "string",
  "user_type": "string",
  "average_rating": number,
  "total_trips_as_passenger": number,
  "total_trips_as_driver": number,
  "created_at": "datetime"
}
```

#### Update Current User Profile
Update authenticated user's information.

```
PUT /api/users/update_profile/
PATCH /api/users/update_profile/  // For partial updates
Body: {
  "first_name": "string",
  "last_name": "string",
  "phone_number": "string",
  "profile_picture": "file",  // Optional
  "bio": "string"             // Optional
}
```

### User Profiles

#### List Users
Get a paginated list of users.

```
GET /api/users/
Query Parameters:
  - page: number (default: 1)
  - page_size: number (default: 20, max: 100)
Response: {
  "count": number,
  "next": "url",
  "previous": "url",
  "results": [User objects]
}
```

#### Get User by ID
Get a specific user's public profile.

```
GET /api/users/{id}/
Response: {User object}
```

#### Get Passenger Profiles
List all passenger profiles.

```
GET /api/users/passengers/
Response: [Passenger profile objects]
```

#### Get Driver Profiles
List all driver profiles.

```
GET /api/users/drivers/
Response: [Driver profile objects]
```

#### Get Top Rated Drivers
Get the highest-rated drivers.

```
GET /api/users/drivers/top_rated/
Query Parameters:
  - limit: number (default: 10)
Response: [Driver objects sorted by rating]
```

#### Set Driver Availability
Update driver's online/offline status.

```
POST /api/users/drivers/{id}/set_availability/
Body: {
  "is_available": boolean
}
```

### Trips

Trips represent ride-sharing journeys from a start location to an end location. Passengers create trips, and drivers can accept and complete them.

#### Trip States
- **pending**: Trip created, waiting for driver
- **accepted**: Driver accepted the trip
- **in_progress**: Trip has started
- **completed**: Trip finished successfully
- **cancelled**: Trip was cancelled

#### Create Trip
Create a new trip request (Passenger only).

```
POST /api/trips/
Body: {
  "start_location_name": "string",       // e.g., "Sofia Airport"
  "start_latitude": number,              // e.g., 42.6977
  "start_longitude": number,             // e.g., 23.3219
  "end_location_name": "string",         // e.g., "Sofia City Center"
  "end_latitude": number,
  "end_longitude": number,
  "passenger_notes": "string",           // Optional notes
  "number_of_passengers": number         // Default: 1
}
Response: {
  "id": number,
  "passenger": User object,
  "driver": null,
  "status": "pending",
  "start_location_name": "string",
  "start_latitude": number,
  "start_longitude": number,
  "end_location_name": "string",
  "end_latitude": number,
  "end_longitude": number,
  "distance_km": number,
  "passenger_notes": "string",
  "number_of_passengers": number,
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

#### List All Trips
Get all trips (admin only).

```
GET /api/trips/
Query Parameters:
  - status: pending|accepted|in_progress|completed|cancelled
  - page: number
Response: {
  "count": number,
  "next": "url",
  "previous": "url",
  "results": [Trip objects]
}
```

#### Get Trip by ID
Get details of a specific trip.

```
GET /api/trips/{id}/
Response: {Trip object}
```

#### Get My Active Trips
Get current user's active trips (not completed or cancelled).

```
GET /api/trips/my_trips/
Response: [Active trip objects]
```

#### Get Available Trips
Get trips available for drivers to accept (status=pending).

```
GET /api/trips/available_trips/
Query Parameters:
  - max_distance_km: number  // Optional: filter by max distance
Response: [Available trip objects]
```

#### Get Trip History
Get historical trips for the current user.

```
GET /api/trips/trip_history/
Query Parameters:
  - role: all|passenger|driver  // Filter by role
  - status: completed|cancelled  // Filter by status
Response: [Trip objects]
```

#### Accept Trip
Accept a pending trip (Driver only).

```
POST /api/trips/{id}/accept/
Response: {
  "message": "Trip accepted successfully",
  "trip": {Trip object}
}
```

#### Start Trip
Mark trip as started (Driver only, must be accepted first).

```
POST /api/trips/{id}/start/
Response: {
  "message": "Trip started successfully",
  "trip": {Trip object}
}
```

#### Complete Trip
Mark trip as completed (Driver only, must be in_progress).

```
POST /api/trips/{id}/complete/
Body: {
  "end_latitude": number,   // Optional actual end location
  "end_longitude": number
}
Response: {
  "message": "Trip completed successfully",
  "trip": {Trip object}
}
```

#### Cancel Trip
Cancel a trip (Passenger can cancel pending trips, Driver can cancel accepted trips).

```
POST /api/trips/{id}/cancel/
Body: {
  "cancellation_reason": "string"  // Optional
}
Response: {
  "message": "Trip cancelled successfully"
}
```

#### Update Trip
Update trip details (limited fields, only before acceptance).

```
PUT /api/trips/{id}/
PATCH /api/trips/{id}/
Body: {
  "passenger_notes": "string",
  "number_of_passengers": number
}
```

#### Delete Trip
Delete a trip (only if status is pending and user is passenger).

```
DELETE /api/trips/{id}/
Response: 204 No Content
```

### Ratings & Reviews

The rating system allows passengers and drivers to review each other after completing a trip. Reviews help maintain service quality and build trust.

#### Rating Scale
- All ratings are on a scale of 1-5 (1 = worst, 5 = best)
- Overall rating is calculated from multiple categories

#### Create Review
Create a review for a completed trip.

```
POST /api/ratings/reviews/
Body: {
  "trip": number,                      // Trip ID
  "reviewed_user": number,             // User being reviewed
  "rating": number,                    // Overall rating (1-5)
  "comment": "string",                 // Optional review text
  "punctuality_rating": number,        // Optional (1-5)
  "cleanliness_rating": number,        // Optional (1-5)
  "safety_rating": number,             // Optional (1-5)
  "communication_rating": number       // Optional (1-5)
}
Response: {
  "id": number,
  "trip": Trip object,
  "reviewer": User object,
  "reviewed_user": User object,
  "rating": number,
  "comment": "string",
  "punctuality_rating": number,
  "cleanliness_rating": number,
  "safety_rating": number,
  "communication_rating": number,
  "created_at": "datetime"
}
```

#### List All Reviews
Get all reviews (paginated).

```
GET /api/ratings/reviews/
Query Parameters:
  - page: number
  - reviewed_user: number  // Filter by reviewed user ID
  - reviewer: number       // Filter by reviewer user ID
  - rating: number         // Filter by minimum rating
Response: {
  "count": number,
  "next": "url",
  "previous": "url",
  "results": [Review objects]
}
```

#### Get Review by ID
Get details of a specific review.

```
GET /api/ratings/reviews/{id}/
Response: {Review object}
```

#### Get My Reviews Received
Get reviews received by the current user.

```
GET /api/ratings/reviews/my_reviews_received/
Response: [Review objects where current user is reviewed]
```

#### Get My Reviews Given
Get reviews given by the current user.

```
GET /api/ratings/reviews/my_reviews_given/
Response: [Review objects where current user is reviewer]
```

#### Get Pending Reviews
Get trips that need to be reviewed by the current user.

```
GET /api/ratings/reviews/pending_reviews/
Response: [
  {
    "trip": Trip object,
    "user_to_review": User object,
    "trip_completed_at": "datetime"
  }
]
```

#### Get User Review Summary
Get aggregated review statistics for a user.

```
GET /api/ratings/reviews/user_summary/
Query Parameters:
  - user_id: number  // Required
Response: {
  "user": User object,
  "total_reviews": number,
  "average_rating": number,
  "average_punctuality": number,
  "average_cleanliness": number,
  "average_safety": number,
  "average_communication": number,
  "rating_distribution": {
    "5": number,  // Count of 5-star reviews
    "4": number,
    "3": number,
    "2": number,
    "1": number
  },
  "recent_reviews": [Review objects]  // Last 5 reviews
}
```

#### Update Review
Update your own review (within 24 hours of creation).

```
PUT /api/ratings/reviews/{id}/
PATCH /api/ratings/reviews/{id}/
Body: {
  "rating": number,
  "comment": "string",
  // ... other rating fields
}
```

#### Delete Review
Delete your own review (within 24 hours of creation).

```
DELETE /api/ratings/reviews/{id}/
Response: 204 No Content
```

## Response Formats

### Success Responses
All successful responses follow these conventions:
- **200 OK**: Successful GET, PUT, PATCH requests
- **201 Created**: Successful POST requests creating resources
- **204 No Content**: Successful DELETE requests

### Error Responses
Error responses include descriptive messages:

```json
{
  "error": "Error message description",
  "detail": "Detailed error information"
}
```

### Validation Errors
Field validation errors return 400 Bad Request:

```json
{
  "field_name": ["Error message for this field"],
  "another_field": ["Error message for another field"]
}
```

## Status Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **204 No Content**: Resource deleted successfully
- **400 Bad Request**: Invalid request data or validation error
- **401 Unauthorized**: Authentication credentials missing or invalid
- **403 Forbidden**: Authenticated but not authorized for this action
- **404 Not Found**: Requested resource doesn't exist
- **500 Internal Server Error**: Server error

## Pagination

List endpoints return paginated results:

```json
{
  "count": 100,           // Total number of items
  "next": "url",          // URL for next page (null if last page)
  "previous": "url",      // URL for previous page (null if first page)
  "results": [...]        // Array of result objects
}
```

Query parameters for pagination:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

Example: `GET /api/users/?page=2&page_size=50`

## Filtering

Many list endpoints support filtering via query parameters. Check the Swagger UI documentation for specific filters available on each endpoint.

Common filters:
- **status**: Filter by status field (e.g., `status=completed`)
- **user_type**: Filter by user type (e.g., `user_type=driver`)
- **created_at**: Filter by creation date

## Rate Limiting

Currently, no rate limiting is enforced in development. Production deployments should implement appropriate rate limiting based on requirements.

## Data Types

### DateTime Format
All datetime fields use ISO 8601 format:
```
"2024-01-29T12:30:00Z"
```

### Location Coordinates
- **Latitude**: Decimal degrees, range -90 to 90
- **Longitude**: Decimal degrees, range -180 to 180

Example:
```json
{
  "latitude": 42.6977,
  "longitude": 23.3219
}
```

## Example Workflows

### Complete Trip Flow

1. **Passenger creates trip**
   ```
   POST /api/trips/
   ```

2. **Driver views available trips**
   ```
   GET /api/trips/available_trips/
   ```

3. **Driver accepts trip**
   ```
   POST /api/trips/{id}/accept/
   ```

4. **Driver starts trip**
   ```
   POST /api/trips/{id}/start/
   ```

5. **Driver completes trip**
   ```
   POST /api/trips/{id}/complete/
   ```

6. **Both parties review each other**
   ```
   POST /api/ratings/reviews/
   ```

### Authentication Flow

1. **Register new user**
   ```
   POST /api/users/
   ```

2. **Login to get tokens**
   ```
   POST /api/users/token/
   ```

3. **Use access token in requests**
   ```
   Authorization: Bearer {access_token}
   ```

4. **Refresh token when expired**
   ```
   POST /api/users/token/refresh/
   ```

## Development & Testing

### Using Swagger UI

1. Start the backend server
2. Navigate to `http://localhost:8000/api/docs/`
3. Click "Authorize" button
4. Enter your access token in format: `Bearer {your_token}`
5. Try out any endpoint with the "Try it out" button

### Using cURL

```bash
# Register a user
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepass123",
    "password2": "securepass123",
    "first_name": "Test",
    "last_name": "User",
    "phone_number": "+1234567890",
    "user_type": "both"
  }'

# Login
curl -X POST http://localhost:8000/api/users/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepass123"
  }'

# Use the access token
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer {access_token}"
```

### Using Postman

1. Import the OpenAPI schema from `http://localhost:8000/api/schema/`
2. Set up environment variables for base URL and tokens
3. Configure Authorization header with Bearer token

## Security Considerations

- **Always use HTTPS in production**
- **Never share access tokens** - treat them like passwords
- **Refresh tokens before expiration** to maintain user sessions
- **Implement proper CORS settings** for web clients
- **Validate all input data** on the client side for better UX
- **Handle 401 responses** by redirecting to login or refreshing token

## Support & Contact

For API issues or questions:
- Check the Swagger UI documentation at `/api/docs/`
- Review the project README and documentation
- Open an issue on the GitHub repository

---

**Version**: 1.0.0  
**Last Updated**: January 2026
