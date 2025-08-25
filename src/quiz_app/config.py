"""
Configuration management for dbt Certification Quiz Application
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class BaseConfig:
    """Base configuration class"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Environment detection
    IS_PRODUCTION = os.environ.get('FLASK_ENV') == 'production' or os.environ.get('RENDER') == 'true'
    IS_DEVELOPMENT = not IS_PRODUCTION
    
    # Application paths
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / 'data'
    QUESTIONS_FILE = DATA_DIR / 'questions.md'
    
    # Quiz settings
    MAX_QUESTIONS = 45
    DEFAULT_QUESTIONS = 10
    DEFAULT_DIFFICULTY = 2
    
    # Google OAuth Configuration
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'your_google_client_id_here')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', 'your_google_client_secret_here')
    
    # Dynamic redirect URI based on environment
    @property
    def GOOGLE_REDIRECT_URI(self):
        if self.IS_PRODUCTION:
            # Get the production URL from environment or use a default
            base_url = os.environ.get('RENDER_EXTERNAL_URL', 'https://your-app-name.onrender.com')
            return f"{base_url}/auth/google/callback"
        else:
            return os.environ.get('GOOGLE_REDIRECT_URI', 'http://localhost:8000/auth/google/callback')
    
    # Google OAuth URLs
    GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
    GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
    GOOGLE_USERINFO_URL = 'https://www.googleapis.com/oauth2/v2/userinfo'
    
    # Scopes for Google OAuth
    GOOGLE_SCOPES = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]
    
    # Razorpay Configuration
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', 'your_razorpay_key_id_here')
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', 'your_razorpay_key_secret_here')


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'
    
    # Production settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'production-secret-key-change-in-production'


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False


def config_from_env():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development').lower()
    
    if env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestingConfig
    else:
        return DevelopmentConfig
