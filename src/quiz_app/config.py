"""
Configuration management for dbt Certification Quiz Application
"""
import os
from pathlib import Path


class BaseConfig:
    """Base configuration class"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Application paths
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / 'data'
    QUESTIONS_FILE = DATA_DIR / 'questions.md'
    
    # Quiz settings
    MAX_QUESTIONS = 45
    DEFAULT_QUESTIONS = 10
    DEFAULT_DIFFICULTY = 2


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'
    
    # Production settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required in production")


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
