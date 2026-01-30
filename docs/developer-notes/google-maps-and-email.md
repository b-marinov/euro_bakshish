# Google Maps API and Email Configuration Guide

This document explains how Google Maps API and email sending are configured and used in the Euro Bakshish project.

## Table of Contents
- [Google Maps API Configuration](#google-maps-api-configuration)
  - [Backend Configuration](#backend-configuration)
  - [Web Frontend Configuration](#web-frontend-configuration)
  - [Android App Configuration](#android-app-configuration)
  - [Setting Up Google Maps API](#setting-up-google-maps-api)
- [Email Configuration](#email-configuration)
  - [Current Email Setup](#current-email-setup)
  - [Configuring Email Providers](#configuring-email-providers)
  - [Testing Email Locally](#testing-email-locally)
- [Security Best Practices](#security-best-practices)

---

## Google Maps API Configuration

### Backend Configuration

The Django backend stores the Google Maps API key in the settings file for server-side use (e.g., geocoding, distance calculations).

**File Location:** `backend/euro_bakshish/settings.py`

```python
# Google Maps
GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY', default='')
```

The API key is loaded from the environment variable `GOOGLE_MAPS_API_KEY` using `python-decouple`.

**Environment File:** `backend/.env`

```env
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

### Web Frontend Configuration

The React web application uses the `@react-google-maps/api` package (version ^2.19.0) for Google Maps integration.

**Package:** Listed in `web/package.json`:
```json
"@react-google-maps/api": "^2.19.0"
```

**Environment Variable:** The API key should be set in the web frontend's environment file.

**File Location:** `web/.env`

```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

**Usage in React:** The API key is typically accessed via `process.env.REACT_APP_GOOGLE_MAPS_API_KEY` and passed to the Google Maps components.

Example usage pattern:
```javascript
import { GoogleMap, LoadScript } from '@react-google-maps/api';

function MapComponent() {
  return (
    <LoadScript googleMapsApiKey={process.env.REACT_APP_GOOGLE_MAPS_API_KEY}>
      <GoogleMap
        // map configuration
      />
    </LoadScript>
  );
}
```

### Android App Configuration

The Android application requires the Google Maps API key to be configured in the AndroidManifest.xml file.

**File Location:** `android/app/src/main/AndroidManifest.xml`

```xml
<meta-data
    android:name="com.google.android.geo.API_KEY"
    android:value="YOUR_GOOGLE_MAPS_API_KEY" />
```

**Note:** Replace `YOUR_GOOGLE_MAPS_API_KEY` with your actual API key. For better security in production, consider using build variants and build configuration fields to inject the key from environment variables during the build process.

### Setting Up Google Maps API

To enable Google Maps functionality in the Euro Bakshish application, follow these steps:

#### 1. Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note your project ID

#### 2. Enable Required APIs

Navigate to **APIs & Services > Library** and enable the following APIs:

- **Maps JavaScript API** - Required for web frontend maps display
- **Geocoding API** - Required for converting addresses to coordinates
- **Distance Matrix API** - Required for calculating trip distances (if used)
- **Places API** - Required for location search and autocomplete (if used)
- **Directions API** - Required for route planning (if used)
- **Maps SDK for Android** - Required for Android app maps display

#### 3. Create API Credentials

1. Go to **APIs & Services > Credentials**
2. Click **Create Credentials > API Key**
3. Copy the generated API key
4. Click on the key name to configure restrictions

#### 4. Configure API Key Restrictions

**For Production:**
- **Application restrictions:**
  - For web: Set HTTP referrers (websites) and add your domain(s)
  - For Android: Set Android apps and add your package name and SHA-1 fingerprint
  - For backend: Set IP addresses for your server IPs

- **API restrictions:**
  - Select "Restrict key"
  - Choose only the APIs you need from the list above

**For Development:**
- You can use unrestricted keys during development, but **never commit them to source control**
- Consider using separate API keys for development and production

#### 5. Set Environment Variables

**Backend:**
```bash
# backend/.env
GOOGLE_MAPS_API_KEY=AIza...your_actual_key_here
```

**Web Frontend:**
```bash
# web/.env
REACT_APP_GOOGLE_MAPS_API_KEY=AIza...your_actual_key_here
```

**Android:**
Edit `android/app/src/main/AndroidManifest.xml` and replace the placeholder with your key.

#### 6. Local Development

For local development:
1. Copy `.env.example` to `.env` in both `backend/` and `web/` directories
2. Add your Google Maps API key to each `.env` file
3. The `.env` files are already listed in `.gitignore` to prevent accidental commits

**Backend:**
```bash
cd backend
cp .env.example .env
# Edit .env and set GOOGLE_MAPS_API_KEY
```

**Web:**
```bash
cd web
cp .env.example .env
# Edit .env and set REACT_APP_GOOGLE_MAPS_API_KEY
```

#### 7. Verify Configuration

- **Backend:** The API key is available via `settings.GOOGLE_MAPS_API_KEY`
- **Web:** Access via `process.env.REACT_APP_GOOGLE_MAPS_API_KEY` in React components
- **Android:** The key is automatically injected by the Android SDK from AndroidManifest.xml

---

## Email Configuration

### Current Email Setup

The Django backend currently uses Django's default email configuration. By default, Django uses a **console backend** which prints emails to the console during development.

**File Location:** `backend/euro_bakshish/settings.py`

Currently, there are **no explicit email configuration settings** in the settings file, which means Django uses these defaults:

```python
# Django defaults (not explicitly set in the project)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
```

The console backend is useful for development as it displays email content in the terminal where `manage.py runserver` is running, without actually sending emails.

### Configuring Email Providers

To send actual emails in production or for testing, you need to configure an SMTP backend or a third-party email service.

#### Option 1: Standard SMTP Configuration

Add these settings to `backend/euro_bakshish/settings.py`:

```python
# Email Configuration
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@eurobakshish.com')
```

Then add to `backend/.env`:

```env
# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@eurobakshish.com
```

**Gmail Example:**
- Use App Passwords (not your regular password): https://myaccount.google.com/apppasswords
- Enable 2-factor authentication first
- HOST: `smtp.gmail.com`, PORT: `587`, TLS: `True`

**Other Common SMTP Providers:**

**Outlook/Office 365:**
```env
EMAIL_HOST=smtp.office365.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

**Yahoo:**
```env
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

**Custom SMTP Server:**
```env
EMAIL_HOST=mail.yourdomain.com
EMAIL_PORT=587  # or 465 for SSL
EMAIL_USE_TLS=True  # or EMAIL_USE_SSL=True for port 465
```

#### Option 2: SendGrid

SendGrid is a popular email service with good free tier and Django integration.

**Installation:**
```bash
pip install sendgrid-django
```

**Configuration in settings.py:**
```python
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = config('SENDGRID_API_KEY', default='')
SENDGRID_SANDBOX_MODE_IN_DEBUG = config('SENDGRID_SANDBOX_MODE_IN_DEBUG', default=True, cast=bool)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@eurobakshish.com')
```

**Environment variables:**
```env
SENDGRID_API_KEY=SG.your_api_key_here
SENDGRID_SANDBOX_MODE_IN_DEBUG=True
DEFAULT_FROM_EMAIL=noreply@eurobakshish.com
```

**Getting SendGrid API Key:**
1. Sign up at https://sendgrid.com/
2. Go to Settings > API Keys
3. Create a new API key with Mail Send permissions
4. Copy the key immediately (it won't be shown again)

#### Option 3: Mailgun

Mailgun is another popular email service.

**Installation:**
```bash
pip install django-mailgun
```

**Configuration in settings.py:**
```python
EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_API_KEY = config('MAILGUN_API_KEY', default='')
MAILGUN_DOMAIN_NAME = config('MAILGUN_DOMAIN_NAME', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@eurobakshish.com')
```

**Environment variables:**
```env
MAILGUN_API_KEY=your-mailgun-api-key
MAILGUN_DOMAIN_NAME=yourdomain.com
DEFAULT_FROM_EMAIL=noreply@eurobakshish.com
```

**Getting Mailgun Credentials:**
1. Sign up at https://www.mailgun.com/
2. Verify your domain or use the sandbox domain
3. Get API key from Settings > API Keys
4. Note your domain name

#### Option 4: Amazon SES

AWS Simple Email Service is cost-effective for high volume.

**Installation:**
```bash
pip install django-ses
```

**Configuration in settings.py:**
```python
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='')
AWS_SES_REGION_NAME = config('AWS_SES_REGION_NAME', default='us-east-1')
AWS_SES_REGION_ENDPOINT = config('AWS_SES_REGION_ENDPOINT', default='email.us-east-1.amazonaws.com')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@eurobakshish.com')
```

### Testing Email Locally

#### Method 1: Console Backend (Current Default)

The console backend prints emails to the terminal - great for development.

**Configuration (already active by default):**
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**Testing:**
```bash
cd backend
python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    'Test Subject',
    'Test message body.',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)
```

The email will be printed to the console where the Django shell is running.

#### Method 2: File Backend

Saves emails to files instead of sending them.

**Configuration in settings.py:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'tmp' / 'emails'
```

**Or via environment:**
```env
EMAIL_BACKEND=django.core.mail.backends.filebased.EmailBackend
```

Emails will be saved as files in `backend/tmp/emails/` directory.

#### Method 3: Local SMTP Server (Python smtpd)

Run a simple SMTP debugging server that prints incoming emails.

**Terminal 1 - Start debugging SMTP server:**
```bash
python -m smtpd -n -c DebuggingServer localhost:1025
```

**Terminal 2 - Configure Django to use it:**

Add to `backend/.env`:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=localhost
EMAIL_PORT=1025
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=False
```

Now emails will be captured and displayed by the debugging server.

#### Method 4: MailHog (Recommended for Teams)

MailHog is a better email testing tool with a web UI.

**Installation:**
```bash
# macOS
brew install mailhog

# Linux
# Download from https://github.com/mailhog/MailHog/releases

# Windows
# Download from https://github.com/mailhog/MailHog/releases
```

**Start MailHog:**
```bash
mailhog
```

**Configure Django:**
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=localhost
EMAIL_PORT=1025
EMAIL_USE_TLS=False
```

**Access Web UI:**
Open http://localhost:8025 to view captured emails.

#### Method 5: Mailtrap

Mailtrap is a cloud-based email testing service.

**Steps:**
1. Sign up at https://mailtrap.io/
2. Get SMTP credentials from your inbox
3. Configure Django:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_HOST_USER=your-mailtrap-username
EMAIL_HOST_PASSWORD=your-mailtrap-password
EMAIL_USE_TLS=True
```

View emails in Mailtrap's web interface.

#### Testing Email Sending

**Using Django Shell:**
```bash
cd backend
python manage.py shell
```

```python
from django.core.mail import send_mail

# Simple email
send_mail(
    'Test Subject',
    'This is a test email from Euro Bakshish.',
    'noreply@eurobakshish.com',
    ['user@example.com'],
    fail_silently=False,
)

# HTML email
from django.core.mail import EmailMultiAlternatives

subject = 'Welcome to Euro Bakshish'
text_content = 'Welcome! Thanks for signing up.'
html_content = '<h1>Welcome!</h1><p>Thanks for signing up.</p>'
msg = EmailMultiAlternatives(subject, text_content, 'noreply@eurobakshish.com', ['user@example.com'])
msg.attach_alternative(html_content, "text/html")
msg.send()
```

**Using Django Management Command (if implemented):**
```bash
python manage.py sendtestemail youremail@example.com
```

---

## Security Best Practices

### 1. Never Commit Secrets to Source Control

**✅ DO:**
- Use `.env` files for local development (already in `.gitignore`)
- Use environment variables in production
- Use secret management services (AWS Secrets Manager, Azure Key Vault, etc.)

**❌ DON'T:**
- Commit API keys directly in code
- Commit `.env` files
- Share credentials in documentation or comments
- Use real production keys in examples

### 2. Restrict API Keys

**Google Maps API:**
- Set application restrictions (HTTP referrers for web, package name for Android)
- Set API restrictions (enable only the APIs you need)
- Use separate keys for development and production
- Rotate keys periodically

### 3. Email Security

**Passwords:**
- Use app-specific passwords (Gmail, Yahoo)
- Never use your main account password
- Use OAuth2 when available
- Rotate passwords periodically

**SMTP Security:**
- Always use TLS/SSL (`EMAIL_USE_TLS=True` or `EMAIL_USE_SSL=True`)
- Use port 587 (TLS) or 465 (SSL), never port 25 unencrypted

### 4. Environment Variables

**Backend (.env file):**
```env
# Add to backend/.env (already in .gitignore)
SECRET_KEY=generate-a-random-secret-key
DEBUG=False  # Never True in production
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
EMAIL_HOST_PASSWORD=your-email-password
```

**Frontend (.env file):**
```env
# Add to web/.env (should be in .gitignore)
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

**Note:** Frontend environment variables are embedded in the built JavaScript bundle and are **not secure**. Only use frontend environment variables for public configuration like API endpoints and public API keys. Never store secrets or private keys in frontend environment variables.

### 5. Production Deployment

**Environment Variables:**
- Use platform-specific environment variable management:
  - Heroku: `heroku config:set KEY=value`
  - AWS: AWS Systems Manager Parameter Store or Secrets Manager
  - Docker: Pass via `docker run -e` or docker-compose environment
  - Kubernetes: ConfigMaps and Secrets

**Monitoring:**
- Monitor API usage in Google Cloud Console
- Set up billing alerts
- Monitor email sending quotas
- Log email failures for debugging

### 6. Example Environment Files

The repository includes `.env.example` files that serve as templates:

**backend/.env.example** - Template for backend environment variables
**web/.env.example** - Template for frontend environment variables

**To use:**
```bash
# Backend
cd backend
cp .env.example .env
# Edit .env with your actual values

# Web
cd web
cp .env.example .env
# Edit .env with your actual values
```

### 7. Security Checklist

- [ ] All API keys stored in environment variables
- [ ] `.env` files listed in `.gitignore`
- [ ] Google Maps API keys restricted by application and API
- [ ] Email passwords are app-specific or use OAuth2
- [ ] TLS/SSL enabled for email (production)
- [ ] Different API keys for development and production
- [ ] Secrets not committed to version control
- [ ] Production `DEBUG=False`
- [ ] Production `ALLOWED_HOSTS` properly configured
- [ ] Regular rotation of API keys and passwords

---

## Additional Resources

**Google Maps Platform:**
- Documentation: https://developers.google.com/maps/documentation
- API Key Best Practices: https://developers.google.com/maps/api-security-best-practices
- Pricing Calculator: https://mapsplatform.google.com/pricing/

**Django Email:**
- Django Email Documentation: https://docs.djangoproject.com/en/stable/topics/email/
- Email Backend Reference: https://docs.djangoproject.com/en/stable/topics/email/#email-backends

**React Google Maps:**
- @react-google-maps/api: https://react-google-maps-api-docs.netlify.app/

**Email Services:**
- SendGrid: https://sendgrid.com/
- Mailgun: https://www.mailgun.com/
- AWS SES: https://aws.amazon.com/ses/
- Mailtrap (testing): https://mailtrap.io/

**Security:**
- OWASP: https://owasp.org/www-project-web-security-testing-guide/
- Django Security: https://docs.djangoproject.com/en/stable/topics/security/

---

## Support

If you encounter issues with Google Maps API or email configuration:

1. Check that environment variables are properly set in `.env` files
2. Verify API keys are valid and not expired
3. Check Google Cloud Console for API usage and errors
4. Review Django logs for email sending errors
5. Ensure required APIs are enabled in Google Cloud Console
6. Verify email provider credentials and quotas

For additional help, refer to the main project documentation or create an issue in the repository.
