# Project Overview - Euro Bakshish

## 📁 Project Structure

```
euro_bakshish/
├── 📱 android/                    # Android Application (Kotlin)
│   ├── app/
│   │   ├── build.gradle          # Android dependencies
│   │   ├── proguard-rules.pro    # Code obfuscation rules
│   │   └── src/main/
│   │       ├── AndroidManifest.xml
│   │       ├── java/com/eurobakshish/
│   │       │   ├── models/       # Data models (User, Trip, Review)
│   │       │   ├── services/     # API service & Retrofit client
│   │       │   ├── ui/           # Activities (Login, Dashboard, etc.)
│   │       │   └── utils/        # PreferenceManager
│   │       └── res/
│   │           └── values/       # String resources
│   ├── gradle/
│   ├── build.gradle              # Project-level Gradle
│   ├── settings.gradle
│   └── README.md
│
├── 🐍 backend/                    # Django REST API
│   ├── apps/
│   │   ├── users/                # User management app
│   │   │   ├── models.py         # User, PassengerProfile, DriverProfile
│   │   │   ├── serializers.py   # API serializers
│   │   │   ├── views.py          # ViewSets for CRUD operations
│   │   │   ├── urls.py           # URL routing
│   │   │   ├── admin.py          # Admin interface
│   │   │   └── tests.py          # Unit tests
│   │   ├── trips/                # Trip management app
│   │   │   ├── models.py         # Trip model
│   │   │   ├── serializers.py   # Trip serializers
│   │   │   ├── views.py          # Trip ViewSets
│   │   │   ├── urls.py
│   │   │   └── admin.py
│   │   └── ratings/              # Rating system app
│   │       ├── models.py         # Review model
│   │       ├── serializers.py   # Review serializers
│   │       ├── views.py          # Review ViewSets
│   │       ├── urls.py
│   │       └── admin.py
│   ├── euro_bakshish/
│   │   ├── settings.py           # Django configuration
│   │   ├── urls.py               # Main URL routing
│   │   ├── wsgi.py               # WSGI application
│   │   └── asgi.py               # ASGI application
│   ├── manage.py                 # Django management script
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example              # Environment variables template
│   ├── pytest.ini                # Test configuration
│   └── README.md
│
├── ⚛️ web/                         # React Web Application
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/           # Reusable components
│   │   │   ├── NavBar.js
│   │   │   └── PrivateRoute.js
│   │   ├── pages/                # Page components
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── Dashboard.js
│   │   │   ├── Profile.js
│   │   │   ├── TripPlanner.js
│   │   │   └── TripHistory.js
│   │   ├── redux/                # State management
│   │   │   ├── store/
│   │   │   │   └── store.js
│   │   │   └── slices/
│   │   │       ├── authSlice.js
│   │   │       └── tripSlice.js
│   │   ├── services/             # API communication
│   │   │   ├── api.js            # Axios configuration
│   │   │   └── services.js       # API methods
│   │   ├── App.js                # Main application
│   │   └── index.js              # Entry point
│   ├── package.json              # Node dependencies
│   ├── .env.example              # Environment variables template
│   └── README.md
│
├── 📚 docs/                       # Documentation
│   ├── API.md                    # API endpoint documentation
│   ├── ARCHITECTURE.md           # System architecture
│   ├── SETUP.md                  # Development setup guide
│   └── SECURITY.md               # Security best practices
│
├── 📄 Root Files
│   ├── README.md                 # Main project README
│   ├── CONTRIBUTING.md           # Contribution guidelines
│   ├── LICENSE                   # MIT License
│   └── .gitignore                # Git ignore rules
```

## 🎯 Core Features

### 1. User Management
- **Registration**: Create accounts as Passenger, Driver, or Both
- **Authentication**: JWT token-based authentication
- **Profiles**: Separate profiles for passengers and drivers
  - Passenger: Payment preferences, emergency contacts, trip history
  - Driver: Vehicle details, license info, availability status

### 2. Trip Management
- **Trip Creation**: Passengers can request trips with start/end locations
- **Trip States**: pending → accepted → in_progress → completed
- **Driver Operations**: Accept, start, and complete trips
- **Trip History**: Complete history for both passengers and drivers
- **Cancellation**: Both parties can cancel trips

### 3. Rating System
- **Mutual Reviews**: Both passengers and drivers rate each other
- **Multi-dimensional Ratings**: Overall + category-specific (punctuality, cleanliness, safety, communication)
- **Automatic Calculations**: User ratings update automatically
- **Review History**: Complete review history for all users

## 🔧 Technology Stack

### Backend
- **Django 4.x**: Python web framework
- **Django REST Framework**: RESTful API
- **PostgreSQL**: Relational database
- **JWT**: Authentication tokens
- **pytest**: Testing framework

### Web Frontend
- **React 18**: UI library
- **Redux Toolkit**: State management
- **Material-UI**: Component library
- **Axios**: HTTP client
- **React Router**: Navigation

### Android
- **Kotlin**: Programming language
- **MVVM**: Architecture pattern
- **Retrofit**: HTTP client
- **Coroutines**: Async operations
- **Material Design**: UI components

## 🚀 Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Edit with your settings
python manage.py migrate
python manage.py runserver
```

### Web
```bash
cd web
npm install
npm start
```

### Android
1. Open `android/` in Android Studio
2. Sync Gradle files
3. Run the application

## 📊 API Endpoints

### Authentication
- `POST /api/users/token/` - Login
- `POST /api/users/token/refresh/` - Refresh token
- `POST /api/users/` - Register
- `GET /api/users/me/` - Current user

### Trips
- `POST /api/trips/` - Create trip
- `GET /api/trips/my_trips/` - Active trips
- `GET /api/trips/trip_history/` - Trip history
- `POST /api/trips/{id}/accept/` - Accept trip
- `POST /api/trips/{id}/start/` - Start trip
- `POST /api/trips/{id}/complete/` - Complete trip
- `POST /api/trips/{id}/cancel/` - Cancel trip

### Ratings
- `POST /api/ratings/reviews/` - Create review
- `GET /api/ratings/reviews/my_reviews_received/` - Reviews received
- `GET /api/ratings/reviews/my_reviews_given/` - Reviews given
- `GET /api/ratings/reviews/pending_reviews/` - Pending reviews
- `GET /api/ratings/reviews/user_summary/` - User rating summary

## 🔒 Security

⚠️ **Important**: Review `docs/SECURITY.md` before production deployment

Key security features:
- JWT token authentication
- Password hashing (PBKDF2)
- Required SECRET_KEY via environment variable
- DEBUG defaults to False
- CORS configuration
- Input validation

## 📖 Documentation

- **[README.md](README.md)**: Main project overview
- **[docs/SETUP.md](docs/SETUP.md)**: Detailed setup instructions
- **[docs/API.md](docs/API.md)**: API endpoint documentation
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**: System architecture
- **[docs/SECURITY.md](docs/SECURITY.md)**: Security best practices
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: How to contribute

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Web tests
cd web
npm test
```

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines

## 👥 Project Status

✅ **Complete** - All core features implemented
- User registration and authentication
- Trip creation and management
- Rating and review system
- Trip history tracking
- Multi-platform support (Web + Android)

---

**Euro Bakshish** - A modern ride-sharing platform 🚗✨
