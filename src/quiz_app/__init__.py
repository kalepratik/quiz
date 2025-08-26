"""
dbt Certification Quiz Application Factory
"""
from flask import Flask
from dotenv import load_dotenv
from .config import config_from_env
from .routes import ui_bp, api_bp

# Load environment variables from .env file
load_dotenv()


def create_app():
    """Application factory pattern"""
    app = Flask(
        __name__, 
        static_folder="../../static", 
        template_folder="../../templates"
    )
    
    # Load configuration
    app.config.from_object(config_from_env())
    
    # Register blueprints
    app.register_blueprint(ui_bp)
    app.register_blueprint(api_bp)
    
    # Suppress development server warning in production-like environments
    if app.config.get('IS_PRODUCTION'):
        import logging
        logging.getLogger('werkzeug').setLevel(logging.ERROR)
    
    # Initialize extensions and services
    from .services.quiz_service import QuizService
    app.quiz_service = QuizService()
    
    return app
