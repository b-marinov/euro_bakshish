# Project Overview - Euro Bakshish

## 📁 Project Structure

```
euro_bakshish/
├── 📱 euro_bakshish_app.py     # Main NextPy Application
│   ├── Database Models         # User, Trip, Review models
│   ├── Application State       # State management
│   ├── API Endpoints          # Automatically generated
│   └── UI Components          # Login, Register, Dashboard, etc.
│
├── 📦 requirements-nextpy.txt  # Python dependencies
│
├── 🗄️ euro_bakshish.db         # SQLite database (auto-created)
│
├── 🗂️ backend/                 # Legacy Django backend (deprecated)
├── 🗂️ web/                     # Legacy React frontend (deprecated)
│
└── 📚 docs/                    # Project documentation
    ├── API.md                  # Legacy API documentation
    ├── ARCHITECTURE.md         # Legacy architecture
    ├── SETUP.md                # Legacy setup guide
    └── SECURITY.md             # Security best practices
```

## 🎯 Architecture Changes

### Previous Architecture (Deprecated)
- **Backend**: Django REST Framework (Python)
- **Frontend**: React + Redux (JavaScript/TypeScript)
- **Android**: Kotlin (Mobile)
- **Database**: PostgreSQL
- **Authentication**: JWT tokens
- **Complexity**: 3 separate codebases, multiple languages, complex deployment

### New Architecture (NextPy-based)
- **Full Stack**: NextPy (Pure Python)
- **Frontend**: React components via Python (no JavaScript!)
- **Backend**: FastAPI (built into NextPy)
- **Database**: SQLModel (SQLite/PostgreSQL)
- **Authentication**: Built-in session management
- **Complexity**: Single codebase, single language, simple deployment

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

### Current Stack (NextPy)
- **NextPy**: Pure Python full-stack framework
- **SQLModel**: SQL database ORM (built on SQLAlchemy + Pydantic)
- **FastAPI**: High-performance API (built into NextPy)
- **React**: UI rendering (via NextPy, no JS needed)
- **SQLite/PostgreSQL**: Database options

### Benefits of NextPy
- **Single Language**: Everything in Python - no context switching
- **Unified Codebase**: Frontend and backend in one file
- **Type Safety**: Pydantic models ensure data validation
- **Auto-Generated API**: REST API created automatically
- **Hot Reload**: Fast development with instant updates
- **Easy Deployment**: Single Python app to deploy
- **AI-Ready**: Built-in support for AI/LLM integration

## 🚀 Quick Start

### Running the Application

```bash
# Install dependencies
pip install -r requirements-nextpy.txt

# Run the application
python euro_bakshish_app.py

# Access at http://localhost:3000
```

That's it! The database is automatically created, and both frontend and backend are running.

## 📊 Core Features

All features from the original application are maintained in the NextPy version:

### 1. User Management
- **Registration**: Create accounts as Passenger, Driver, or Both
- **Authentication**: Secure session-based authentication
- **Profiles**: User profile management with all necessary fields
  - Passenger: Payment preferences, emergency contacts
  - Driver: Vehicle details, license info, availability status

### 2. Trip Management
- **Trip Creation**: Passengers request trips with start/end locations
- **Trip States**: pending → accepted → in_progress → completed
- **Driver Operations**: Accept, start, and complete trips
- **Trip History**: Complete history for both passengers and drivers
- **Cancellation**: Trip cancellation support

### 3. Rating System
- **Mutual Reviews**: Both passengers and drivers rate each other
- **Multi-dimensional Ratings**: Overall + category-specific ratings
- **Automatic Calculations**: User ratings update automatically
- **Review History**: Complete review history for all users

## 🎨 User Interface

The NextPy application provides a clean, modern web interface with:

- **Login/Register Pages**: User authentication
- **Dashboard**: Main user interface
- **Trip Management**: Create and view trips
- **Profile Pages**: User profile management
- **Trip History**: View past trips and ratings

All UI is built with Python - no JavaScript required!

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
