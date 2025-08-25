"""
OAuth Service for Google Authentication
"""
import os
import requests
import logging
from urllib.parse import urlencode
from flask import current_app, session

logger = logging.getLogger(__name__)

class OAuthService:
    """Service for handling Google OAuth authentication"""
    
    @staticmethod
    def get_google_auth_url():
        """Generate Google OAuth authorization URL"""
        try:
            # Debug logging
            logger.info(f"Client ID: {current_app.config['GOOGLE_CLIENT_ID']}")
            
            # Simple redirect URI - use environment variable or default
            redirect_uri = os.environ.get('GOOGLE_REDIRECT_URI', 'http://localhost:8000/auth/google/callback')
            logger.info(f"Redirect URI: {redirect_uri}")
            logger.info(f"Scopes: {current_app.config['GOOGLE_SCOPES']}")
            logger.info(f"Scopes: {current_app.config['GOOGLE_SCOPES']}")
            
            params = {
                'client_id': current_app.config['GOOGLE_CLIENT_ID'],
                'redirect_uri': redirect_uri,
                'scope': ' '.join(current_app.config['GOOGLE_SCOPES']),
                'response_type': 'code',
                'access_type': 'offline',
                'prompt': 'consent'
            }
            
            auth_url = f"{current_app.config['GOOGLE_AUTH_URL']}?{urlencode(params)}"
            logger.info(f"Generated Google OAuth URL: {auth_url}")
            return auth_url
            
        except Exception as e:
            logger.error(f"Error generating Google OAuth URL: {e}")
            return None
    
    @staticmethod
    def exchange_code_for_token(auth_code):
        """Exchange authorization code for access token"""
        try:
            # Simple redirect URI - use environment variable or default
            redirect_uri = os.environ.get('GOOGLE_REDIRECT_URI', 'http://localhost:8000/auth/google/callback')
            
            token_data = {
                'client_id': current_app.config['GOOGLE_CLIENT_ID'],
                'client_secret': current_app.config['GOOGLE_CLIENT_SECRET'],
                'code': auth_code,
                'grant_type': 'authorization_code',
                'redirect_uri': redirect_uri
            }
            
            response = requests.post(
                current_app.config['GOOGLE_TOKEN_URL'],
                data=token_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            if response.status_code == 200:
                token_info = response.json()
                logger.info("Successfully exchanged code for token")
                return token_info
            else:
                logger.error(f"Token exchange failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error exchanging code for token: {e}")
            return None
    
    @staticmethod
    def get_user_info(access_token):
        """Get user information from Google"""
        try:
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(
                current_app.config['GOOGLE_USERINFO_URL'],
                headers=headers
            )
            
            if response.status_code == 200:
                user_info = response.json()
                logger.info(f"Retrieved user info for: {user_info.get('email')}")
                return user_info
            else:
                logger.error(f"Failed to get user info: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return None
    
    @staticmethod
    def authenticate_user(auth_code):
        """Complete OAuth flow and return user data"""
        try:
            # Exchange code for token
            token_info = OAuthService.exchange_code_for_token(auth_code)
            if not token_info:
                return None
            
            # Get user information
            user_info = OAuthService.get_user_info(token_info['access_token'])
            if not user_info:
                return None
            
            # Store user data in session
            session['user_id'] = user_info['id']
            session['user_email'] = user_info['email']
            session['user_name'] = user_info.get('name', user_info['email'])
            session['user_picture'] = user_info.get('picture')
            session['is_authenticated'] = True
            
            logger.info(f"User authenticated: {user_info['email']}")
            return user_info
            
        except Exception as e:
            logger.error(f"Error in authentication flow: {e}")
            return None
    
    @staticmethod
    def logout_user():
        """Logout user by clearing session"""
        try:
            session.clear()
            logger.info("User logged out")
            return True
        except Exception as e:
            logger.error(f"Error during logout: {e}")
            return False
    
    @staticmethod
    def is_user_authenticated():
        """Check if user is authenticated"""
        return session.get('is_authenticated', False)
    
    @staticmethod
    def get_current_user():
        """Get current user information from session"""
        if OAuthService.is_user_authenticated():
            return {
                'id': session.get('user_id'),
                'email': session.get('user_email'),
                'name': session.get('user_name'),
                'picture': session.get('user_picture')
            }
        return None
