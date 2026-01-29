# Development Setup Guide

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python 3.10+**
- **Node.js 18+** and npm
- **PostgreSQL 13+**
- **Android Studio** (for Android development)
- **Git**

## Backend Setup

### 1. Navigate to backend directory
```bash
cd backend
```

### 2. Create and activate virtual environment
```bash
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
# Copy the example env file
cp .env.example .env

# Edit .env file with your settings
# Update database credentials, secret key, etc.
```

### 5. Setup PostgreSQL database
```bash
# Create database (run in PostgreSQL shell or command line)
createdb euro_bakshish

# Or using psql:
psql -U postgres
CREATE DATABASE euro_bakshish;
\q
```

### 6. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create superuser
```bash
python manage.py createsuperuser
```

### 8. Run development server
```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000/api/`
Admin panel at: `http://localhost:8000/admin/`
API Documentation at: `http://localhost:8000/api/docs/`

## Web Frontend Setup

### 1. Navigate to web directory
```bash
cd web
```

### 2. Install dependencies
```bash
npm install
```

### 3. Configure environment (optional)
```bash
# Create .env file in web directory
echo "REACT_APP_API_URL=http://localhost:8000/api" > .env
```

### 4. Start development server
```bash
npm start
```

The web application will be available at: `http://localhost:3000`

## Android Setup

### 1. Open Android Studio
Launch Android Studio and select "Open an Existing Project"

### 2. Open the project
Navigate to and select the `android` directory

### 3. Sync Gradle files
Android Studio will automatically sync Gradle files. If not, click:
`File > Sync Project with Gradle Files`

### 4. Configure API URL
Edit `android/app/src/main/java/com/eurobakshish/services/RetrofitClient.kt`
```kotlin
private const val BASE_URL = "http://10.0.2.2:8000/api/" // For emulator
// OR
private const val BASE_URL = "http://YOUR_IP:8000/api/" // For physical device
```

### 5. Add Google Maps API Key
Edit `android/app/src/main/AndroidManifest.xml` and replace:
```xml
<meta-data
    android:name="com.google.android.geo.API_KEY"
    android:value="YOUR_GOOGLE_MAPS_API_KEY" />
```

### 6. Run the application
- Select a device/emulator
- Click the Run button (green play icon)

## Testing the Application

### Backend Tests
```bash
cd backend
pytest
```

### Web Tests
```bash
cd web
npm test
```

## Common Issues and Solutions

### Issue: Database connection error
**Solution**: Verify PostgreSQL is running and credentials in `.env` are correct

### Issue: Port already in use
**Solution**: Kill the process using the port or use a different port:
```bash
# Backend
python manage.py runserver 8001

# Web
PORT=3001 npm start
```

### Issue: Module not found (Python)
**Solution**: Ensure virtual environment is activated and dependencies are installed

### Issue: Cannot connect to API from Android
**Solution**: 
- For emulator: Use `10.0.2.2` instead of `localhost`
- For physical device: Use your computer's IP address
- Ensure backend server is running

## Development Workflow

1. **Backend changes**: Edit Python files, Django will auto-reload
2. **Web changes**: Edit React files, hot reload is enabled
3. **Android changes**: Edit Kotlin files, rebuild the app

## Database Management

### Create new migrations
```bash
python manage.py makemigrations
```

### Apply migrations
```bash
python manage.py migrate
```

### Reset database
```bash
python manage.py flush
```

### Create sample data
```bash
python manage.py shell
# Then run commands to create test data
```

## Production Deployment

See individual deployment guides:
- Backend: Deploy to Heroku, AWS, or DigitalOcean
- Web: Deploy to Vercel, Netlify, or any static hosting
- Android: Build APK/AAB and publish to Google Play Store

For production:
1. Set `DEBUG=False` in Django settings
2. Configure proper `ALLOWED_HOSTS`
3. Use environment variables for all secrets
4. Enable HTTPS
5. Set up proper database backups
6. Configure proper CORS settings
