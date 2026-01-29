# Euro Bakshish Android

Android application for the Euro Bakshish ride-sharing platform.

## Quick Start

1. Open project in Android Studio
2. Sync Gradle files
3. Update API URL in `RetrofitClient.kt`
4. Add Google Maps API key in `AndroidManifest.xml`
5. Run the application

## Requirements

- Android Studio Arctic Fox or later
- Android SDK 24+ (Android 7.0)
- Kotlin 1.9.20+

## Configuration

### API URL
Edit `app/src/main/java/com/eurobakshish/services/RetrofitClient.kt`:
```kotlin
private const val BASE_URL = "http://10.0.2.2:8000/api/" // For emulator
```

### Google Maps
Add your API key in `app/src/main/AndroidManifest.xml`:
```xml
<meta-data
    android:name="com.google.android.geo.API_KEY"
    android:value="YOUR_API_KEY" />
```

## Technology Stack

- Kotlin
- MVVM Architecture
- Retrofit for networking
- Coroutines for async operations
- Material Design
- Google Maps SDK
