"""
Flask routes for dbt Certification Quiz Application
"""
import json
import logging
from flask import Blueprint, render_template, request, jsonify, current_app
from .services.quiz_service import QuizService

# Create blueprints
ui_bp = Blueprint('ui', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Setup logging
logger = logging.getLogger(__name__)


@ui_bp.route('/')
def index():
    """Main quiz interface"""
    return render_template('index.html')


@ui_bp.route('/healthz')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'dbt-certification-quiz',
        'version': '1.0.0'
    }), 200


@api_bp.route('/configure-quiz')
def configure_quiz():
    """API endpoint for quiz configuration"""
    try:
        # Get parameters
        num_questions = request.args.get('num_questions', type=int, default=10)
        difficulty = request.args.get('difficulty', type=int, default=2)
        
        # Validate parameters
        if not (1 <= num_questions <= current_app.config['MAX_QUESTIONS']):
            num_questions = current_app.config['DEFAULT_QUESTIONS']
        
        if not (1 <= difficulty <= 5):
            difficulty = current_app.config['DEFAULT_DIFFICULTY']
        
        # Get quiz service
        quiz_service = current_app.quiz_service
        
        # Generate quiz configuration
        config = quiz_service.get_quiz_config(num_questions, difficulty)
        
        logger.info(f"Quiz configured: {num_questions} questions, difficulty {difficulty}")
        return jsonify(config)
        
    except Exception as e:
        logger.error(f"Error configuring quiz: {e}")
        return jsonify({'error': 'Failed to configure quiz'}), 500


@api_bp.route('/quiz-config')
def quiz_config():
    """Legacy endpoint for backward compatibility"""
    return configure_quiz()


@api_bp.route('/question-stats')
def question_stats():
    """API endpoint for question statistics"""
    try:
        # Get quiz service
        quiz_service = current_app.quiz_service
        
        # Get question statistics
        stats = quiz_service.get_question_stats()
        
        logger.info(f"Question stats requested: {stats}")
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Error getting question stats: {e}")
        return jsonify({'error': 'Failed to get question stats'}), 500
