# API Documentation

## Base URL
`http://localhost:8000/api/`

## Authentication
All endpoints except login and register require JWT token authentication.

Include the token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## Endpoints

### Authentication

#### Login
```
POST /users/token/
Body: {
  "username": "string",
  "password": "string"
}
Response: {
  "access": "string",
  "refresh": "string"
}
```

#### Register
```
POST /users/
Body: {
  "username": "string",
  "email": "string",
  "password": "string",
  "password2": "string",
  "first_name": "string",
  "last_name": "string",
  "phone_number": "string",
  "user_type": "passenger|driver|both"
}
```

#### Get Current User
```
GET /users/me/
```

### Trips

#### Create Trip
```
POST /trips/
Body: {
  "start_location_name": "string",
  "start_latitude": number,
  "start_longitude": number,
  "end_location_name": "string",
  "end_latitude": number,
  "end_longitude": number,
  "passenger_notes": "string",
  "number_of_passengers": number
}
```

#### Get My Active Trips
```
GET /trips/my_trips/
```

#### Get Trip History
```
GET /trips/trip_history/?role=all|passenger|driver
```

#### Accept Trip (Driver only)
```
POST /trips/{id}/accept/
```

#### Start Trip (Driver only)
```
POST /trips/{id}/start/
```

#### Complete Trip (Driver only)
```
POST /trips/{id}/complete/
```

#### Cancel Trip
```
POST /trips/{id}/cancel/
```

### Ratings

#### Create Review
```
POST /ratings/reviews/
Body: {
  "trip": number,
  "reviewed_user": number,
  "rating": number (1-5),
  "comment": "string",
  "punctuality_rating": number (1-5),
  "cleanliness_rating": number (1-5),
  "safety_rating": number (1-5),
  "communication_rating": number (1-5)
}
```

#### Get My Reviews Received
```
GET /ratings/reviews/my_reviews_received/
```

#### Get My Reviews Given
```
GET /ratings/reviews/my_reviews_given/
```

#### Get Pending Reviews
```
GET /ratings/reviews/pending_reviews/
```

#### Get User Review Summary
```
GET /ratings/reviews/user_summary/?user_id={id}
```

## Status Codes
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error
