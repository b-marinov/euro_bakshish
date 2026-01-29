# Security Considerations

This document outlines important security considerations for the Euro Bakshish application.

## Backend Security

### Secret Key
- **NEVER** commit the SECRET_KEY to version control
- Use environment variables to store the SECRET_KEY
- Generate a strong, random secret key for production
- The application will fail to start if SECRET_KEY is not set

### DEBUG Mode
- DEBUG is set to False by default
- Only enable DEBUG=True in development environments
- Never deploy with DEBUG=True in production

### Database Credentials
- Store database credentials in environment variables
- Never commit database credentials to version control
- Use strong passwords for database users
- Limit database user permissions to only what's needed

### JWT Tokens
- Access tokens expire after 60 minutes by default
- Refresh tokens expire after 24 hours by default
- Configure these durations based on your security requirements

### HTTPS
- **Always** use HTTPS in production
- Configure SSL/TLS certificates properly
- Use HSTS (HTTP Strict Transport Security)

### CORS
- Configure CORS to only allow trusted domains
- Never use wildcard (*) origins in production
- List specific allowed origins in the environment variable

## Web Frontend Security

### Token Storage
⚠️ **Important**: The current implementation stores JWT tokens in localStorage, which is vulnerable to XSS attacks.

**Recommended Improvements:**
1. Store tokens in httpOnly cookies (requires backend changes)
2. Implement Content Security Policy (CSP)
3. Use SameSite cookie attributes
4. Implement proper input sanitization

**Current Mitigation:**
- Keep dependencies updated
- Follow secure coding practices
- Implement CSP headers
- Sanitize all user inputs

### API Communication
- All API requests should use HTTPS in production
- Tokens are automatically included in Authorization header
- Expired tokens trigger automatic refresh

### Input Validation
- Client-side validation is implemented but not sufficient
- Server-side validation is the authoritative source
- Validate all user inputs before submission

## Android Security

### Token Storage
⚠️ **Important**: The current implementation stores tokens in SharedPreferences without encryption.

**Recommended Improvements:**
1. Use EncryptedSharedPreferences:
```kotlin
val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .build()

val encryptedPrefs = EncryptedSharedPreferences.create(
    context,
    "secure_prefs",
    masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)
```

2. Use Android Keystore for sensitive data

### Network Security
⚠️ **Important**: usesCleartextTraffic is enabled for development.

**Production Configuration:**
- Set `android:usesCleartextTraffic="false"` in AndroidManifest.xml
- Use HTTPS for all API communication
- Implement certificate pinning for added security

### Logging
- Logging level is reduced in production builds
- Sensitive data should never be logged
- Remove all debug logs before release

### API Key Protection
- Google Maps API key should be restricted in Google Cloud Console
- Use Android app restrictions
- Implement key rotation policy

## General Security Best Practices

### Password Requirements
Enforce strong passwords:
- Minimum 8 characters
- Mix of uppercase, lowercase, numbers, and special characters
- Django's built-in validators are configured

### Rate Limiting
**Recommended Implementation:**
- Limit login attempts
- Implement rate limiting on API endpoints
- Use django-ratelimit or similar library

### Input Sanitization
- All user inputs are validated on the backend
- SQL injection protection via Django ORM
- XSS protection via proper output encoding

### Authentication
- JWT tokens are used for authentication
- Passwords are hashed using Django's default PBKDF2
- Never store plain text passwords

### Authorization
- Permissions are checked on all API endpoints
- Users can only access their own data
- Admin users have elevated permissions

### Error Handling
- Don't expose sensitive information in error messages
- Log errors for debugging but show generic messages to users
- Handle exceptions gracefully

## Security Checklist for Production

### Backend
- [ ] SECRET_KEY is set via environment variable
- [ ] DEBUG=False in production
- [ ] HTTPS is enabled and enforced
- [ ] Database uses strong credentials
- [ ] CORS is properly configured
- [ ] Implement rate limiting
- [ ] Configure security headers
- [ ] Set up monitoring and logging
- [ ] Regular security updates

### Web Frontend
- [ ] API URL points to HTTPS endpoint
- [ ] Content Security Policy is implemented
- [ ] Dependencies are up to date
- [ ] Input validation is implemented
- [ ] Consider implementing httpOnly cookies
- [ ] Regular security audits

### Android
- [ ] usesCleartextTraffic is false
- [ ] Implement EncryptedSharedPreferences
- [ ] Google Maps API key is restricted
- [ ] ProGuard/R8 is enabled
- [ ] Code obfuscation is configured
- [ ] Certificate pinning is implemented
- [ ] Regular security updates

## Reporting Security Issues

If you discover a security vulnerability, please:
1. **Do not** open a public issue
2. Email the security team directly
3. Provide detailed information about the vulnerability
4. Allow time for the issue to be fixed before disclosure

## Regular Maintenance

- Keep all dependencies updated
- Monitor security advisories
- Perform regular security audits
- Implement automated security scanning
- Review and update security policies regularly

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [React Security Best Practices](https://reactjs.org/docs/dom-elements.html#dangerouslysetinnerhtml)
- [Android Security Best Practices](https://developer.android.com/topic/security/best-practices)
