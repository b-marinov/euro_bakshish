# Architecture Overview

## System Architecture

Euro Bakshish is a three-tier ride-sharing application consisting of:

1. **Backend API** (Django REST Framework)
2. **Web Frontend** (React)
3. **Mobile Application** (Android - Kotlin)

## Backend Architecture

### Technology Stack
- **Framework**: Django 4.x with Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)

### Application Structure
```
backend/
├── euro_bakshish/          # Project configuration
│   ├── settings.py         # Django settings
│   ├── urls.py             # URL routing
│   └── wsgi.py             # WSGI configuration
├── apps/
│   ├── users/              # User management
│   │   ├── models.py       # User, PassengerProfile, DriverProfile
│   │   ├── views.py        # API views
│   │   ├── serializers.py  # Data serialization
│   │   └── urls.py         # URL patterns
│   ├── trips/              # Trip management
│   │   ├── models.py       # Trip model
│   │   ├── views.py        # Trip CRUD operations
│   │   └── serializers.py  # Trip serialization
│   └── ratings/            # Rating system
│       ├── models.py       # Review model
│       ├── views.py        # Review operations
│       └── serializers.py  # Review serialization
└── manage.py               # Django management script
```

### Key Models

#### User Model
- Extends Django's AbstractUser
- Fields: username, email, user_type (passenger/driver/both), phone, profile_picture
- Related profiles: PassengerProfile, DriverProfile

#### Trip Model
- Represents a ride from point A to point B
- Status flow: pending → accepted → in_progress → completed
- Tracks locations, timestamps, fare, and participants

#### Review Model
- Links to Trip and Users
- Ratings: overall + category-specific (punctuality, cleanliness, safety, communication)
- Updates user average ratings automatically

## Web Frontend Architecture

### Technology Stack
- **Framework**: React 18
- **State Management**: Redux Toolkit
- **UI Library**: Material-UI
- **Routing**: React Router v6
- **HTTP Client**: Axios

### Application Structure
```
web/
├── src/
│   ├── components/         # Reusable UI components
│   │   ├── NavBar.js
│   │   └── PrivateRoute.js
│   ├── pages/              # Page components
│   │   ├── Login.js
│   │   ├── Register.js
│   │   ├── Dashboard.js
│   │   ├── Profile.js
│   │   ├── TripPlanner.js
│   │   └── TripHistory.js
│   ├── redux/              # State management
│   │   ├── store/          # Redux store
│   │   └── slices/         # Redux slices
│   ├── services/           # API services
│   │   ├── api.js          # Axios configuration
│   │   └── services.js     # API methods
│   └── App.js              # Main application
└── public/
    └── index.html
```

### State Management
- **Auth Slice**: User authentication state
- **Trip Slice**: Active trips and trip history
- JWT tokens stored in localStorage
- Automatic token refresh on 401 responses

## Android Application Architecture

### Technology Stack
- **Language**: Kotlin
- **Architecture**: MVVM (Model-View-ViewModel)
- **Networking**: Retrofit + OkHttp
- **Asynchronous**: Coroutines
- **UI**: Material Design

### Application Structure
```
android/app/src/main/java/com/eurobakshish/
├── models/                 # Data models
│   ├── User.kt
│   ├── Trip.kt
│   └── Review.kt
├── services/               # API services
│   ├── ApiService.kt       # Retrofit interface
│   └── RetrofitClient.kt   # Retrofit setup
├── ui/                     # UI components
│   ├── MainActivity.kt
│   ├── login/
│   ├── register/
│   ├── dashboard/
│   ├── trips/
│   └── profile/
└── utils/                  # Utility classes
    └── PreferenceManager.kt
```

## Data Flow

### Trip Creation Flow
1. **Passenger** creates trip request via web/mobile app
2. Request sent to backend API
3. Trip saved to database with status "pending"
4. **Driver** views pending trips
5. Driver accepts trip (status → "accepted")
6. Driver starts trip (status → "in_progress")
7. Driver completes trip (status → "completed")
8. Trip counts updated for both users
9. Both users can now review each other

### Rating Flow
1. Trip must be completed
2. Passenger/Driver creates review
3. Review linked to trip and users
4. Average rating automatically updated
5. Rating displayed on user profiles

## Security Considerations

- JWT tokens for authentication
- Password hashing (Django default PBKDF2)
- CORS configured for allowed origins
- HTTPS recommended for production
- Environment variables for sensitive data
- Database credentials never committed to version control

## Database Schema

### Users App
- User (extends AbstractUser)
- PassengerProfile (one-to-one with User)
- DriverProfile (one-to-one with User)

### Trips App
- Trip (many-to-one with User for both passenger and driver)

### Ratings App
- Review (many-to-one with Trip, many-to-one with User)

## API Design Principles

- RESTful architecture
- JWT token authentication
- Consistent error responses
- Pagination for list endpoints
- Filtering and searching capabilities
- Automatic API documentation (Swagger/OpenAPI)
