"""
Flask routes for dbt Certification Quiz Application
"""
import json
import logging
from flask import Blueprint, render_template, request, jsonify, current_app, redirect, url_for, session
from .services.quiz_service import QuizService
from .services.oauth_service import OAuthService

# Create blueprints
ui_bp = Blueprint('ui', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Setup logging
logger = logging.getLogger(__name__)

# Context processor to pass environment info to all templates
@ui_bp.context_processor
def inject_environment():
    """Inject environment variables into template context"""
    from .config import config_from_env
    config_class = config_from_env()
    config_instance = config_class()
    logger.debug(f"Environment: IS_PRODUCTION={config_instance.IS_PRODUCTION}, IS_DEVELOPMENT={config_instance.IS_DEVELOPMENT}")
    return {
        'is_production': config_instance.IS_PRODUCTION,
        'is_development': config_instance.IS_DEVELOPMENT
    }


@ui_bp.route('/')
def index():
    """Landing page with modern UI"""
    return render_template('homepage.html')

@ui_bp.route('/quiz')
def quiz():
    """Main quiz interface"""
    return render_template('index.html')

@ui_bp.route('/homepage')
def homepage():
    """Landing page with modern UI (alias)"""
    return render_template('homepage.html')

@ui_bp.route('/signin')
def signin():
    """Sign in page with authentication options"""
    return render_template('signin.html')

@ui_bp.route('/payment')
def payment():
    """Payment page for Pro upgrade"""
    return render_template('payment.html')

@ui_bp.route('/legal')
def legal():
    """Legal information page with Privacy Policy, Terms & Conditions, and Cancellation Policy"""
    return render_template('legal.html')

@ui_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form page"""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            subject = request.form.get('subject', '').strip()
            message = request.form.get('message', '').strip()
            
            # Validate required fields
            if not all([name, email, subject, message]):
                return render_template('contact.html', error='All fields are required.')
            
            # Basic email validation
            if '@' not in email or '.' not in email:
                return render_template('contact.html', error='Please enter a valid email address.')
            
            # Import email service
            from .services.email_service import EmailService
            email_service = EmailService()
            
            # Send email to admin
            admin_email_sent = email_service.send_contact_form_email(name, email, subject, message)
            
            # Send auto-reply to user
            auto_reply_sent = email_service.send_auto_reply(email, name)
            
            if admin_email_sent:
                return render_template('contact.html', success=True)
            else:
                return render_template('contact.html', error='Failed to send message. Please try again later.')
                
        except Exception as e:
            logger.error(f"Error processing contact form: {str(e)}")
            return render_template('contact.html', error='An error occurred. Please try again later.')
    
    return render_template('contact.html')

# OAuth Routes
@ui_bp.route('/auth/google')
def google_auth():
    """Initiate Google OAuth flow"""
    try:
        logger.info("Google OAuth initiation started")
        
        # Check if Google OAuth is configured
        client_id = current_app.config.get('GOOGLE_CLIENT_ID', 'your_google_client_id_here')
        logger.info(f"Google OAuth Client ID: {client_id}")
        
        if not client_id or client_id == 'your_google_client_id_here':
            logger.warning("Google OAuth not configured - using demo mode")
            # In demo mode, simulate successful authentication
            session['user_id'] = 'demo_user_123'
            session['user_email'] = 'demo@example.com'
            session['user_name'] = 'Demo User'
            session['is_authenticated'] = True
            logger.info("Demo mode authentication successful, redirecting to quiz")
            return redirect(url_for('ui.quiz'))
        
        try:
            auth_url = OAuthService.get_google_auth_url()
            logger.info(f"Generated auth URL: {auth_url}")
            if auth_url:
                logger.info("Redirecting to Google OAuth")
                return redirect(auth_url)
            else:
                logger.error("Failed to generate Google OAuth URL")
                return redirect(url_for('ui.signin'))
        except Exception as oauth_error:
            logger.error(f"OAuth service error: {oauth_error}")
            return redirect(url_for('ui.signin'))
    except Exception as e:
        logger.error(f"Error in Google OAuth initiation: {e}")
        return redirect(url_for('ui.signin'))

@ui_bp.route('/auth/google/callback')
def google_auth_callback():
    """Handle Google OAuth callback"""
    try:
        auth_code = request.args.get('code')
        if not auth_code:
            logger.error("No authorization code received")
            return redirect(url_for('ui.signin'))
        
        # Authenticate user
        user_info = OAuthService.authenticate_user(auth_code)
        if user_info:
            logger.info(f"User authenticated successfully: {user_info['email']}")
            return redirect(url_for('ui.quiz'))
        else:
            logger.error("Authentication failed")
            return redirect(url_for('ui.signin'))
            
    except Exception as e:
        logger.error(f"Error in Google OAuth callback: {e}")
        return redirect(url_for('ui.signin'))

@ui_bp.route('/auth/logout')
def logout():
    """Logout user"""
    try:
        OAuthService.logout_user()
        return redirect(url_for('ui.index'))
    except Exception as e:
        logger.error(f"Error during logout: {e}")
        return redirect(url_for('ui.index'))

@api_bp.route('/user-info')
def user_info():
    """Get current user information"""
    try:
        user = OAuthService.get_current_user()
        if user:
            return jsonify({
                'authenticated': True,
                'user': user
            })
        else:
            return jsonify({
                'authenticated': False,
                'user': None
            })
    except Exception as e:
        logger.error(f"Error getting user info: {e}")
        return jsonify({
            'authenticated': False,
            'user': None
        }), 500


@ui_bp.route('/healthz')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'dbt-certification-quiz',
        'version': '1.0.0'
    }), 200


@api_bp.route('/configure-quiz', methods=['GET', 'POST'])
def configure_quiz():
    """API endpoint for quiz configuration"""
    try:
        logger.info(f"Configure quiz called with method: {request.method}")
        
        # Handle both GET and POST requests
        if request.method == 'POST':
            # Get JSON data from POST request
            data = request.get_json()
            logger.info(f"POST data received: {data}")
            if not data:
                return jsonify({'error': 'No JSON data provided'}), 400
            
            question_count = data.get('questionCount', 10)
            difficulty = data.get('difficulty', 2)
        else:
            # Get parameters from GET request
            question_count = request.args.get('num_questions', type=int, default=10)
            difficulty = request.args.get('difficulty', type=int, default=2)
        
        logger.info(f"Parameters: question_count={question_count}, difficulty={difficulty}")
        
        # Validate parameters
        if not (1 <= question_count <= current_app.config['MAX_QUESTIONS']):
            question_count = current_app.config['DEFAULT_QUESTIONS']
        
        if not (1 <= difficulty <= 3):
            difficulty = current_app.config['DEFAULT_DIFFICULTY']
        
        logger.info(f"Validated parameters: question_count={question_count}, difficulty={difficulty}")
        
        # Get quiz service
        quiz_service = current_app.quiz_service
        logger.info(f"Quiz service: {quiz_service}")
        
        # Generate quiz configuration
        config = quiz_service.get_quiz_config(question_count, difficulty)
        logger.info(f"Quiz config generated with {len(config.get('questions', []))} questions")
        
        logger.info(f"Quiz configured: {question_count} questions, difficulty {difficulty}")
        return jsonify(config)
        
    except Exception as e:
        logger.error(f"Error configuring quiz: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Failed to configure quiz'}), 500


@api_bp.route('/quiz-config', methods=['GET', 'POST'])
def quiz_config():
    """Legacy endpoint for backward compatibility"""
    return configure_quiz()

@api_bp.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    """API endpoint for quiz submission and scoring"""
    try:
        logger.info("Submit quiz called")
        
        # Get JSON data from POST request
        data = request.get_json()
        logger.info(f"Submit quiz data received: {data}")
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        answers = data.get('answers', [])
        questions = data.get('questions', [])
        
        if not answers or not questions:
            return jsonify({'error': 'Missing answers or questions data'}), 400
        
        logger.info(f"Processing {len(answers)} answers for {len(questions)} questions")
        
        # Get quiz service
        quiz_service = current_app.quiz_service
        
        # Calculate results
        correct_answers = 0
        total_questions = len(questions)
        
        for i, (question, user_answer) in enumerate(zip(questions, answers)):
            if user_answer is not None:  # Only count answered questions
                # Get correct answer from question (stored as 'correctAnswer' with 0-based index)
                correct_answer = question.get('correctAnswer', 0)  # Default to 0 (A)
                
                if user_answer == correct_answer:
                    correct_answers += 1
                    logger.debug(f"Question {i+1}: Correct")
                else:
                    logger.debug(f"Question {i+1}: Incorrect (user: {user_answer}, correct: {correct_answer})")
        
        result = {
            'correctAnswers': correct_answers,
            'totalQuestions': total_questions,
            'percentage': round((correct_answers / total_questions) * 100, 1) if total_questions > 0 else 0
        }
        
        logger.info(f"Quiz submitted successfully: {correct_answers}/{total_questions} correct")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error submitting quiz: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Failed to submit quiz'}), 500


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
