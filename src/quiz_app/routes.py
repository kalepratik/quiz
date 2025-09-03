"""
Flask routes for dbt Certification Quiz Application
"""
import json
import logging
import time
from flask import Blueprint, render_template, request, jsonify, current_app, redirect, url_for, session
from .services.quiz_service import QuizService
from .services.oauth_service import OAuthService
from .services.payment_service import PaymentService

# Create blueprints
ui_bp = Blueprint('ui', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Setup logging
logger = logging.getLogger(__name__)

# Context processor to pass environment info to all templates
@ui_bp.context_processor
def inject_environment():
    """Inject environment variables into template context"""
    # Get current user info for header
    user = OAuthService.get_current_user()
    is_authenticated = user is not None
    is_pro_user = user.get('is_pro', False) if user else False
    user_name = user.get('name', '').split(' ')[0] if user and user.get('name') else None
    
    return {
        'is_production': False,
        'is_development': True,
        'is_authenticated': is_authenticated,
        'is_pro_user': is_pro_user,
        'user_name': user_name
    }


@ui_bp.route('/')
def index():
    """Landing page with modern UI - redirects PRO users to PRO homepage"""
    # Check if user is authenticated and is PRO
    user = OAuthService.get_current_user()
    if user and user.get('is_pro', False):
        # Redirect PRO users to PRO homepage
        return redirect(url_for('ui.pro_homepage'))
    
    return render_template('homepage.html', active_page='homepage')

@ui_bp.route('/pro-homepage')
def pro_homepage():
    """PRO homepage for paid users"""
    # Check if user is authenticated
    user = OAuthService.get_current_user()
    if not user:
        return redirect(url_for('ui.signin'))
    
    # Check if user is PRO
    if not user.get('is_pro', False):
        return redirect(url_for('ui.payment'))
    
    return render_template('pro-homepage.html', active_page='pro-homepage')

@ui_bp.route('/quiz')
def quiz():
    """Main quiz interface"""
    return render_template('index.html', active_page='quiz')

@ui_bp.route('/quiz-pro')
def quiz_pro():
    """PRO quiz interface for paid users"""
    # Check if user is authenticated
    user = OAuthService.get_current_user()
    if not user:
        return redirect(url_for('ui.signin'))
    
    # Check if user is PRO
    if not user.get('is_pro', False):
        return redirect(url_for('ui.payment'))
    
    return render_template('quiz-pro.html', active_page='quiz-pro')

@ui_bp.route('/history')
def history():
    """Quiz history page for PRO users"""
    # Check if user is authenticated
    user = OAuthService.get_current_user()
    if not user:
        return redirect(url_for('ui.signin'))
    
    # Check if user is PRO
    if not user.get('is_pro', False):
        return redirect(url_for('ui.payment'))
    
    return render_template('history.html', active_page='history')

@ui_bp.route('/dashboard')
def dashboard():
    """Detailed dashboard with analytics for PRO users"""
    # Check if user is authenticated
    user = OAuthService.get_current_user()
    if not user:
        return redirect(url_for('ui.signin'))
    
    # Check if user is PRO
    if not user.get('is_pro', False):
        return redirect(url_for('ui.payment'))
    
    return render_template('dashboard.html', active_page='dashboard')

@ui_bp.route('/homepage')
def homepage():
    """Landing page with modern UI (alias)"""
    return render_template('homepage.html', active_page='homepage')

@ui_bp.route('/signin')
def signin():
    """Sign in page with authentication options"""
    return render_template('signin.html', active_page='signin')

@ui_bp.route('/payment')
def payment():
    """Payment page for Pro upgrade"""
    return render_template('payment.html', active_page='payment')

@api_bp.route('/create-payment-order', methods=['POST'])
def create_payment_order():
    """Create a new payment order"""
    try:
        # Check if user is authenticated (allow test user in development)
        user = OAuthService.get_current_user()
        if not user:
            if current_app.config.get('FLASK_ENV') == 'development':
                # Create a test user for development
                user = {
                    'id': 'test_user_123',
                    'email': 'test@example.com',
                    'name': 'Test User'
                }
                logger.info("Using test user for development payment testing")
            else:
                return jsonify({'error': 'User not authenticated'}), 401
        
        # Get payment amount from request
        data = request.get_json()
        amount = data.get('amount', 300)  # Default to ₹300
        
        # Create payment service
        payment_service = PaymentService()
        
        # Create order
        try:
            order = payment_service.create_order(
                amount=amount,
                receipt_id=f"user_{user['id']}_{int(time.time())}"
            )
            
            return jsonify({
                'success': True,
                'order_id': order['id'],
                'amount': order['amount'],
                'currency': order['currency'],
                'razorpay_key': current_app.config.get('RAZORPAY_KEY_ID')
            })
        except Exception as e:
            logger.error(f"Payment service error: {e}")
            return jsonify({'error': str(e)}), 500
            
    except Exception as e:
        logger.error(f"Error creating payment order: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/verify-payment', methods=['POST'])
def verify_payment():
    """Verify payment and upgrade user to Pro"""
    try:
        # Check if user is authenticated (allow test user in development)
        user = OAuthService.get_current_user()
        if not user:
            if current_app.config.get('FLASK_ENV') == 'development':
                # Create a test user for development
                user = {
                    'id': 'test_user_123',
                    'email': 'test@example.com',
                    'name': 'Test User'
                }
                logger.info("Using test user for development payment verification")
            else:
                return jsonify({'error': 'User not authenticated'}), 401
        
        # Get payment details from request
        data = request.get_json()
        payment_id = data.get('razorpay_payment_id')
        order_id = data.get('razorpay_order_id')
        signature = data.get('razorpay_signature')
        
        if not all([payment_id, order_id, signature]):
            return jsonify({'error': 'Missing payment details'}), 400
        
        # Create payment service
        payment_service = PaymentService()
        
        # Verify payment (allow mock verification in development)
        payment_verified = False
        if current_app.config.get('FLASK_ENV') == 'development':
            # In development, accept any payment for testing
            payment_verified = True
            logger.info("Development mode: Accepting payment for testing")
        else:
            # In production, verify payment properly
            payment_verified = payment_service.verify_payment(payment_id, order_id, signature)
        
        if payment_verified:
            # Payment verified - upgrade user to Pro
            try:
                # Get database service
                db_service = current_app.database_service
                
                # Upgrade user to PRO
                upgraded_user = db_service.upgrade_to_pro(
                    user['id'],
                    {
                        'payment_id': payment_id,
                        'order_id': order_id,
                        'amount': 300,  # Default amount
                        'currency': 'INR',
                        'payment_method': 'razorpay'
                    }
                )
                
                if upgraded_user:
                    # Update session with PRO status
                    session['is_pro'] = True
                    logger.info(f"User {user['email']} upgraded to Pro after payment {payment_id}")
                    
                    return jsonify({
                        'success': True,
                        'message': 'Payment verified and account upgraded to Pro!'
                    })
                else:
                    logger.error(f"Failed to upgrade user {user['email']} to Pro")
                    return jsonify({'error': 'Failed to upgrade account'}), 500
                    
            except Exception as e:
                logger.error(f"Error upgrading user to Pro: {e}")
                return jsonify({'error': 'Failed to upgrade account'}), 500
        else:
            return jsonify({'error': 'Payment verification failed'}), 400
            
    except Exception as e:
        logger.error(f"Error verifying payment: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@ui_bp.route('/legal')
def legal():
    """Legal information page with Privacy Policy, Terms & Conditions, and Cancellation Policy"""
    return render_template('legal.html', active_page='legal')

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
                return render_template('contact.html', active_page='contact', error='All fields are required.')
            
            # Basic email validation
            if '@' not in email or '.' not in email:
                return render_template('contact.html', active_page='contact', error='Please enter a valid email address.')
            
            # Import email service
            from .services.email_service import EmailService
            email_service = EmailService()
            
            # Send email to admin
            admin_email_sent = email_service.send_contact_form_email(name, email, subject, message)
            
            # Send auto-reply to user
            auto_reply_sent = email_service.send_auto_reply(email, name)
            
            if admin_email_sent:
                return render_template('contact.html', active_page='contact', success=True)
            else:
                return render_template('contact.html', active_page='contact', error='Failed to send message. Please try again later.')
                
        except Exception as e:
            logger.error(f"Error processing contact form: {str(e)}")
            return render_template('contact.html', active_page='contact', error='An error occurred. Please try again later.')
    
    return render_template('contact.html', active_page='contact')

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
            logger.error("Google OAuth not configured")
            return redirect(url_for('ui.signin'))
        
        # Generate OAuth URL
        auth_url = OAuthService.get_google_auth_url()
        logger.info(f"Generated auth URL: {auth_url}")
        if auth_url:
            logger.info("Redirecting to Google OAuth")
            return redirect(auth_url)
        else:
            logger.error("Failed to generate Google OAuth URL")
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
            return redirect(url_for('ui.index'))
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
            # In development mode, return a test user
            if current_app.config.get('FLASK_ENV') == 'development':
                test_user = {
                    'id': 'test_user_123',
                    'email': 'test@example.com',
                    'name': 'Test User'
                }
                return jsonify({
                    'authenticated': True,
                    'user': test_user
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
        'version': '1.0.0',
        'environment': current_app.config.get('FLASK_ENV', 'unknown'),
        'debug': current_app.config.get('DEBUG', False),
        'is_development': current_app.config.get('FLASK_ENV') == 'development'
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
        
        # Record quiz attempt in database if user is authenticated
        try:
            user = OAuthService.get_current_user()
            if user:
                db_service = current_app.database_service
                
                # Determine if this is a PRO quiz based on question count
                is_pro_quiz = total_questions > 10  # More than 10 questions indicates PRO quiz
                
                # Prepare detailed questions data for storage
                questions_data = []
                for i, (question, user_answer) in enumerate(zip(questions, answers)):
                    questions_data.append({
                        'question': question,
                        'user_answer': user_answer
                    })
                
                # Record the attempt with detailed data
                quiz_attempt = db_service.record_quiz_attempt(
                    user_id=user['id'],
                    question_count=total_questions,
                    difficulty=2,  # Default difficulty - could be enhanced
                    correct_answers=correct_answers,
                    total_questions=total_questions,
                    percentage=result['percentage'],
                    is_pro_quiz=is_pro_quiz,
                    questions_data=questions_data
                )
                
                if quiz_attempt:
                    logger.info(f"Quiz attempt recorded for user {user['email']}")
                else:
                    logger.warning(f"Failed to record quiz attempt for user {user['email']}")
                    
        except Exception as e:
            logger.error(f"Error recording quiz attempt: {e}")
            # Don't fail the quiz submission if recording fails
        
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

# User Management API Endpoints
@api_bp.route('/user/profile')
def get_user_profile():
    """Get current user profile"""
    try:
        user = OAuthService.get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        # Get database service
        db_service = current_app.database_service
        
        # Get user from database
        db_user = db_service.get_user_by_id(user['id'])
        if not db_user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'user': db_user.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Error getting user profile: {e}")
        return jsonify({'error': 'Failed to get user profile'}), 500

@api_bp.route('/user/stats')
def get_user_stats():
    """Get current user statistics"""
    try:
        user = OAuthService.get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        # Get database service
        db_service = current_app.database_service
        
        # Get user statistics
        stats = db_service.get_user_stats(user['id'])
        if stats is None:
            return jsonify({'error': 'Failed to get user stats'}), 500
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        logger.error(f"Error getting user stats: {e}")
        return jsonify({'error': 'Failed to get user stats'}), 500

@api_bp.route('/user/topic-analysis')
def get_user_topic_analysis():
    """Get current user's topic analysis with weak areas and strengths (last 10 days)"""
    try:
        user = OAuthService.get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        # Get database service
        db_service = current_app.database_service
        
        # Get topic analysis (weak areas and strengths)
        topic_analysis = db_service.get_user_topic_analysis(user['id'])
        
        return jsonify({
            'success': True,
            'topic_analysis': topic_analysis
        })
        
    except Exception as e:
        logger.error(f"Error getting user topic analysis: {e}")
        return jsonify({'error': 'Failed to get topic analysis'}), 500

@api_bp.route('/topic-categories')
def get_topic_categories():
    """Get all available topic categories from the question bank"""
    try:
        # Get database service
        db_service = current_app.database_service
        
        # Get available topic categories
        categories = db_service.get_available_topic_categories()
        
        return jsonify({
            'success': True,
            'categories': categories
        })
        
    except Exception as e:
        logger.error(f"Error getting topic categories: {e}")
        return jsonify({'error': 'Failed to get topic categories'}), 500

@api_bp.route('/user/topic-performance')
def get_user_topic_performance():
    """Get current user's performance across ALL topics (for debugging)"""
    try:
        user = OAuthService.get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        # Get database service
        db_service = current_app.database_service
        
        # Get all topic performance (not just weak ones)
        all_topics = db_service.get_user_all_topic_performance(user['id'])
        
        return jsonify({
            'success': True,
            'all_topics': all_topics
        })
        
    except Exception as e:
        logger.error(f"Error getting user topic performance: {e}")
        return jsonify({'error': 'Failed to get topic performance'}), 500

@api_bp.route('/user/quiz-history')
def get_user_quiz_history():
    """Get current user quiz history"""
    try:
        user = OAuthService.get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        # Get limit from query parameters
        limit = request.args.get('limit', type=int, default=10)
        
        # Get database service
        db_service = current_app.database_service
        
        # Get quiz history
        history = db_service.get_user_quiz_history(user['id'], limit)
        
        return jsonify({
            'success': True,
            'history': [attempt.to_dict() for attempt in history]
        })
        
    except Exception as e:
        logger.error(f"Error getting user quiz history: {e}")
        return jsonify({'error': 'Failed to get quiz history'}), 500

@api_bp.route('/user/check-pro-access')
def check_pro_access():
    """Check if current user has PRO access"""
    try:
        user = OAuthService.get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        # Get database service
        db_service = current_app.database_service
        
        # Check PRO access
        has_pro_access = db_service.check_pro_access(user['id'])
        
        return jsonify({
            'success': True,
            'has_pro_access': has_pro_access
        })
        
    except Exception as e:
        logger.error(f"Error checking PRO access: {e}")
        return jsonify({'error': 'Failed to check PRO access'}), 500

@api_bp.route('/user/subscriptions')
def get_user_subscriptions():
    """Get current user subscriptions"""
    try:
        user = OAuthService.get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        # Get database service
        db_service = current_app.database_service
        
        # Get user subscriptions
        subscriptions = db_service.get_user_subscriptions(user['id'])
        
        return jsonify({
            'success': True,
            'subscriptions': [sub.to_dict() for sub in subscriptions]
        })
        
    except Exception as e:
        logger.error(f"Error getting user subscriptions: {e}")
        return jsonify({'error': 'Failed to get subscriptions'}), 500

@api_bp.route('/user/download-attempt-pdf/<int:attempt_id>')
def download_attempt_pdf(attempt_id):
    """Download PDF summary of a specific quiz attempt"""
    try:
        user = OAuthService.get_current_user()
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        
        # Get database service
        db_service = current_app.database_service
        
        # Get the specific attempt
        attempt = db_service.get_quiz_attempt_by_id(attempt_id)
        if not attempt:
            return jsonify({'error': 'Quiz attempt not found'}), 404
        
        # Verify the attempt belongs to the current user
        if attempt.user_id != user['id']:
            return jsonify({'error': 'Access denied'}), 403
        
        # Get detailed attempt data
        attempt_details = db_service.get_quiz_attempt_details(attempt_id)
        
        # Import PDF service
        from .services.pdf_service import PDFService
        pdf_service = PDFService()
        
        # Convert attempt to dict for PDF generation
        attempt_data = attempt.to_dict()
        
        # Generate PDF with detailed data
        pdf_content = pdf_service.generate_quiz_attempt_pdf(attempt_data, attempt_details)
        
        # Create response with PDF content
        from flask import Response
        response = Response(pdf_content, mimetype='application/pdf')
        response.headers['Content-Disposition'] = f'attachment; filename=quiz-attempt-{attempt_id}.pdf'
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating PDF for attempt {attempt_id}: {e}")
        return jsonify({'error': 'Failed to generate PDF'}), 500
