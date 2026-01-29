# Screenshots

This directory contains screenshots for the Euro Bakshish user tutorial.

## Current Status

The current images are **placeholder screenshots** created programmatically. They serve as visual aids in the tutorial but should be replaced with actual application screenshots.

## Replacing Placeholders with Real Screenshots

To capture and replace these placeholder images with actual screenshots:

### Web Application Screenshots

1. **Start the application:**
   ```bash
   docker-compose up -d
   # or
   make up
   ```

2. **Navigate to http://localhost in your browser**

3. **Capture the following screens:**
   - `web-login.png` - Login page (http://localhost/login)
   - `web-register.png` - Registration page (http://localhost/register)
   - `web-dashboard.png` - Dashboard after login (http://localhost/dashboard)
   - `web-profile.png` - Profile page (http://localhost/profile)
   - `web-trip-planner.png` - Trip planner page (http://localhost/trip-planner)
   - `web-trip-history.png` - Trip history page (http://localhost/trip-history)

4. **Screenshot Tips:**
   - Use your browser's built-in screenshot tool or extensions
   - Recommended resolution: 1200x800 pixels or similar
   - Use PNG format for better quality
   - Capture the full page content
   - Consider using dummy data that looks realistic

### Android Application Screenshots

1. **Build and run the Android app:**
   - Open the `android/` directory in Android Studio
   - Run the app on an emulator or physical device

2. **Capture the following screens:**
   - `android-login.png` - Login screen
   - `android-login-filled.png` - Login screen with credentials filled in
   - `android-dashboard.png` - Main dashboard
   - `android-trip-planner.png` - Trip planning screen
   - `android-trip-history.png` - Trip history screen

3. **Screenshot Tips:**
   - Use Android Studio's screenshot tool or device screenshot function
   - Recommended resolution: 600x1000 pixels (portrait mode)
   - Use PNG format
   - Ensure clear visibility of UI elements
   - Consider showing various states (empty, with data, etc.)

## Image Guidelines

When replacing placeholders:

- **Format**: PNG (preferred) or JPEG
- **Web screenshots**: ~1200x800 pixels (landscape)
- **Android screenshots**: ~600x1000 pixels (portrait)
- **File size**: Keep under 500KB per image
- **Content**: Use realistic but anonymized data
- **Quality**: High DPI/retina displays preferred

## Naming Convention

Keep the existing filenames when replacing:
- `web-*.png` - Web application screenshots
- `android-*.png` - Android application screenshots

## Privacy Note

When capturing screenshots:
- Use test accounts, not real user data
- Anonymize any personal information
- Don't include real names, addresses, or phone numbers
- Use generic email addresses (test@example.com)

## Contributing

If you capture high-quality screenshots:
1. Replace the placeholder images in this directory
2. Commit your changes
3. Update this README if you add new screenshots
4. Submit a pull request

Thank you for improving the documentation! 📸
