# Project Overview - Euro Bakshish

## 📁 Project Structure

```
euro_bakshish/
├── 🗂️ backend/                  # Django REST Framework backend
│   ├── apps/                    # Django applications
│   │   ├── users/              # User management
│   │   ├── trips/              # Trip management
│   │   └── ratings/            # Rating system
│   ├── euro_bakshish/          # Project settings
│   ├── manage.py               # Django management script
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile              # Backend container
│
├── 🗂️ web/                      # React frontend
│   ├── src/                    # Source code
│   │   ├── components/         # React components
│   │   ├── redux/              # State management
│   │   ├── services/           # API services
│   │   └── pages/              # Page components
│   ├── package.json            # Node dependencies
│   └── Dockerfile              # Frontend container
│
├── 📦 docker-compose.yml        # Docker orchestration
│
└── 📚 docs/                     # Project documentation
    ├── API.md                   # API documentation
    ├── ARCHITECTURE.md          # System architecture
    ├── SETUP.md                 # Setup guide
    ├── DOCKER.md                # Docker guide
    └── SECURITY.md              # Security practices
```

## 🎯 Architecture

### Current Architecture
- **Backend**: Django REST Framework (Python)
- **Frontend**: React + Redux (JavaScript/TypeScript)
- **Database**: PostgreSQL
- **Authentication**: JWT tokens
- **API**: RESTful with OpenAPI/Swagger documentation
- **Deployment**: Docker containers orchestrated with Docker Compose

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

- **Django**: Python web framework
- **Django REST Framework**: RESTful API toolkit
- **PostgreSQL**: Relational database
- **React**: Frontend UI library
- **Redux**: State management
- **Docker**: Containerization
- **Nginx**: Reverse proxy (in production)

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Start all services
docker compose up -d

# Access at:
# - Web: http://localhost
# - API: http://localhost:8000/api/
# - Admin: http://localhost:8000/admin/
```

### Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Frontend:**
```bash
cd web
npm install
npm start
```

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
- CORS configuration
- Input validation
- SQL injection protection

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

# Frontend tests
cd web
npm test
```

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines

## 👥 Project Status

✅ **Active** - Django + React stack
- User registration and authentication
- Trip creation and management
- Rating and review system
- Trip history tracking
- Web interface

---

**Euro Bakshish** - A modern ride-sharing platform 🚗✨
