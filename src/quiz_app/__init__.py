"""
dbt Certification Quiz Application Factory
"""
from flask import Flask
from dotenv import load_dotenv
from .config import config_from_env
from .routes import ui_bp, api_bp
from .models import db

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
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(ui_bp)
    app.register_blueprint(api_bp)
    
    # Initialize extensions and services
    from .services.quiz_service import QuizService
    from .services.database_service import DatabaseService
    
    app.quiz_service = QuizService()
    app.database_service = DatabaseService()
    
    # Create database tables (if they don't exist)
    with app.app_context():
        try:
            db.create_all()
            app.logger.info("Database tables verified/created successfully")
        except Exception as e:
            app.logger.error(f"Database initialization error: {e}")
    
    return app
