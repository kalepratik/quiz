# Google OAuth Integration Setup Guide

This guide will help you integrate Google OAuth authentication into your dbt Certification Quiz application.

## Prerequisites

- A Google Cloud Platform account
- Python 3.7+ installed
- Flask application running

## Step 1: Set up Google Cloud Project

### 1.1 Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter a project name (e.g., "dbt-quiz-oauth")
4. Click "Create"

### 1.2 Enable Google+ API

1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Google+ API" or "Google Identity"
3. Click on "Google Identity" and enable it

### 1.3 Configure OAuth Consent Screen

1. Go to "APIs & Services" → "OAuth consent screen"
2. Choose "External" user type
3. Fill in the required information:
   - **App name**: "dbt Certification Quiz"
   - **User support email**: Your email address
   - **Developer contact information**: Your email address
4. Click "Save and Continue"
5. Skip "Scopes" section, click "Save and Continue"
6. Add test users if needed, click "Save and Continue"
7. Review and click "Back to Dashboard"

### 1.4 Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client IDs"
3. Choose "Web application"
4. Fill in the details:
   - **Name**: "dbt-quiz-web-client"
   - **Authorized redirect URIs**:
     - For development: `http://localhost:8000/auth/google/callback`
     - For production: `https://your-domain.com/auth/google/callback`
5. Click "Create"
6. **Save the Client ID and Client Secret** - you'll need these for the next step

## Step 2: Configure Environment Variables

### 2.1 Create Environment File

Create a `.env` file in your project root:

```bash
# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# Flask Configuration
SECRET_KEY=your_secret_key_here

# For development:
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

# For production:
# GOOGLE_REDIRECT_URI=https://your-domain.com/auth/google/callback
```

### 2.2 Install Required Packages

```bash
pip install -r requirements.txt
```

## Step 3: Test the Integration

### 3.1 Start the Application

```bash
python main.py
```

### 3.2 Test the OAuth Flow

1. Open your browser and go to `http://localhost:8000`
2. Click "Sign In"
3. Click "Continue with Google"
4. You should be redirected to Google's OAuth consent screen
5. Sign in with your Google account
6. Grant permissions
7. You should be redirected back to the quiz page

## Step 4: Production Deployment

### 4.1 Update Redirect URIs

1. Go back to Google Cloud Console
2. Update your OAuth 2.0 Client ID
3. Add your production domain to authorized redirect URIs:
   - `https://your-domain.com/auth/google/callback`

### 4.2 Environment Variables

Set these environment variables on your production server:

```bash
export GOOGLE_CLIENT_ID=your_google_client_id_here
export GOOGLE_CLIENT_SECRET=your_google_client_secret_here
export SECRET_KEY=your_production_secret_key_here
export GOOGLE_REDIRECT_URI=https://your-domain.com/auth/google/callback
```

### 4.3 Security Considerations

1. **Never commit your `.env` file** to version control
2. **Use strong secret keys** for production
3. **Enable HTTPS** in production
4. **Set up proper session management**
5. **Monitor OAuth usage** in Google Cloud Console

## Troubleshooting

### Common Issues

1. **"Invalid redirect URI" error**
   - Check that your redirect URI exactly matches what's configured in Google Cloud Console
   - Ensure no trailing slashes or extra characters

2. **"Client ID not found" error**
   - Verify your `GOOGLE_CLIENT_ID` environment variable is set correctly
   - Check that the OAuth 2.0 Client ID is enabled

3. **"Access blocked" error**
   - Add your email as a test user in the OAuth consent screen
   - Ensure the Google+ API is enabled

4. **Session not persisting**
   - Check that `SECRET_KEY` is set
   - Verify session configuration in Flask

### Debug Mode

To enable debug logging, set:

```bash
export FLASK_ENV=development
export LOG_LEVEL=DEBUG
```

## API Endpoints

The following endpoints are now available:

- `GET /auth/google` - Initiate Google OAuth flow
- `GET /auth/google/callback` - Handle OAuth callback
- `GET /auth/logout` - Logout user
- `GET /api/user-info` - Get current user information

## Security Best Practices

1. **Validate redirect URIs** on the server side
2. **Use HTTPS** in production
3. **Implement CSRF protection**
4. **Set secure session cookies**
5. **Log authentication events**
6. **Implement rate limiting**
7. **Regular security audits**

## Support

If you encounter issues:

1. Check the application logs
2. Verify Google Cloud Console configuration
3. Test with a simple OAuth flow first
4. Check Google's OAuth documentation

## Additional Resources

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Flask Session Documentation](https://flask.palletsprojects.com/en/2.0.x/quickstart/#sessions)
- [Google Cloud Console](https://console.cloud.google.com/)
