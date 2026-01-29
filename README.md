# Euro Bakshish - Ride Sharing Application

A comprehensive ride-sharing platform with web and Android applications.

## Features

- **User Profiles**: Create and manage profiles as either a passenger or driver
- **Trip Planning**: Select start and end locations for trips
- **Trip Completion**: Complete trips with mutual ratings between passengers and drivers
- **Trip History**: Track complete history of all trips for both drivers and passengers
- **Rating System**: Maintain user ratings based on reviews from completed trips

## Project Structure

```
euro_bakshish/
├── backend/          # Django REST API backend
├── web/              # React web frontend
├── android/          # Android application
└── docs/             # Project documentation
```

## Technology Stack

### Backend
- **Framework**: Django 4.x with Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT tokens

### Web Frontend
- **Framework**: React 18.x
- **State Management**: Redux
- **UI Library**: Material-UI
- **Maps**: Google Maps API

### Android
- **Language**: Kotlin
- **Architecture**: MVVM
- **Networking**: Retrofit
- **Maps**: Google Maps SDK

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Android Studio (for Android development)
- PostgreSQL

### Quick Setup

See [docs/SETUP.md](docs/SETUP.md) for detailed setup instructions.

### Security

⚠️ **Important**: Please review [docs/SECURITY.md](docs/SECURITY.md) before deploying to production.

Key security considerations:
- Set SECRET_KEY via environment variable (required)
- Use HTTPS in production
- Review token storage mechanisms
- Configure CORS properly
- Keep dependencies updated

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Web Frontend Setup

```bash
cd web
npm install
npm start
```

### Android Setup

1. Open Android Studio
2. Open the `android` directory as a project
3. Sync Gradle files
4. Run the application

## API Documentation

API documentation is available at `/api/docs/` when running the backend server.

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
