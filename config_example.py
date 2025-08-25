# Google OAuth Configuration Example
# Copy this to config.py and fill in your actual values

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Google OAuth Configuration
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', 'your_google_client_id_here')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', 'your_google_client_secret_here')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your_secret_key_here')
    
    # OAuth Redirect URIs
    GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:8000/auth/google/callback')
    
    # Google OAuth URLs
    GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
    GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
    GOOGLE_USERINFO_URL = 'https://www.googleapis.com/oauth2/v2/userinfo'
    
    # Scopes for Google OAuth
    GOOGLE_SCOPES = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]

# Environment variables you need to set:
# GOOGLE_CLIENT_ID=your_google_client_id_here
# GOOGLE_CLIENT_SECRET=your_google_client_secret_here
# FLASK_SECRET_KEY=your_secret_key_here
# GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback (for development)
