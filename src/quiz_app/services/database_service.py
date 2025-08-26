"""
Database service for managing users and subscriptions
"""
import logging
from datetime import datetime, timedelta
from flask import current_app
from ..models import db, User, Subscription, QuizAttempt

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service class for database operations"""
    
    def __init__(self):
        self.db = db
    
    def init_db(self):
        """Initialize database tables"""
        try:
            with current_app.app_context():
                self.db.create_all()
                logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def get_user_by_email(self, email):
        """Get user by email"""
        try:
            return User.query.filter_by(email=email).first()
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            return None
    
    def get_user_by_google_id(self, google_id):
        """Get user by Google ID"""
        try:
            return User.query.filter_by(google_id=google_id).first()
        except Exception as e:
            logger.error(f"Error getting user by Google ID {google_id}: {e}")
            return None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        try:
            return User.query.get(user_id)
        except Exception as e:
            logger.error(f"Error getting user by ID {user_id}: {e}")
            return None
    
    def create_user(self, email, name, google_id=None, profile_picture=None):
        """Create a new user"""
        try:
            user = User(
                email=email,
                name=name,
                google_id=google_id,
                profile_picture=profile_picture,
                is_pro=False
            )
            self.db.session.add(user)
            self.db.session.commit()
            logger.info(f"User created successfully: {email}")
            return user
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Error creating user {email}: {e}")
            return None
    
    def update_user(self, user_id, **kwargs):
        """Update user information"""
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return None
            
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            
            user.updated_at = datetime.utcnow()
            self.db.session.commit()
            logger.info(f"User updated successfully: {user_id}")
            return user
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Error updating user {user_id}: {e}")
            return None
    
    def upgrade_to_pro(self, user_id, payment_data):
        """Upgrade user to PRO and create subscription record"""
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return None
            
            # Create subscription record
            subscription = Subscription(
                user_id=user_id,
                razorpay_payment_id=payment_data['payment_id'],
                razorpay_order_id=payment_data['order_id'],
                amount=payment_data['amount'],
                currency=payment_data.get('currency', 'INR'),
                status='completed',
                payment_method=payment_data.get('payment_method'),
                subscription_start=datetime.utcnow(),
                subscription_end=datetime.utcnow() + timedelta(days=365)  # 1 year subscription
            )
            
            # Update user to PRO
            user.is_pro = True
            user.updated_at = datetime.utcnow()
            
            self.db.session.add(subscription)
            self.db.session.commit()
            
            logger.info(f"User upgraded to PRO successfully: {user_id}")
            return user
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Error upgrading user to PRO {user_id}: {e}")
            return None
    
    def get_user_subscriptions(self, user_id):
        """Get all subscriptions for a user"""
        try:
            return Subscription.query.filter_by(user_id=user_id).order_by(Subscription.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Error getting subscriptions for user {user_id}: {e}")
            return []
    
    def get_active_subscription(self, user_id):
        """Get active subscription for a user"""
        try:
            now = datetime.utcnow()
            return Subscription.query.filter(
                Subscription.user_id == user_id,
                Subscription.status == 'completed',
                Subscription.subscription_end > now
            ).order_by(Subscription.created_at.desc()).first()
        except Exception as e:
            logger.error(f"Error getting active subscription for user {user_id}: {e}")
            return None
    
    def record_quiz_attempt(self, user_id, question_count, difficulty, correct_answers, 
                          total_questions, percentage, is_pro_quiz=False, questions_data=None):
        """Record a quiz attempt with optional detailed data"""
        try:
            quiz_attempt = QuizAttempt(
                user_id=user_id,
                question_count=question_count,
                difficulty=difficulty,
                correct_answers=correct_answers,
                total_questions=total_questions,
                percentage=percentage,
                is_pro_quiz=is_pro_quiz
            )
            self.db.session.add(quiz_attempt)
            self.db.session.flush()  # Get the ID without committing
            
            # Record detailed data if provided
            if questions_data and quiz_attempt.id:
                self._record_quiz_details(quiz_attempt.id, questions_data)
            
            self.db.session.commit()
            logger.info(f"Quiz attempt recorded for user {user_id}")
            return quiz_attempt
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Error recording quiz attempt for user {user_id}: {e}")
            return None
    
    def _record_quiz_details(self, quiz_attempt_id, questions_data):
        """Record detailed quiz attempt data using question IDs"""
        try:
            from ..models import QuizAttemptDetail, Question
            
            for i, question_data in enumerate(questions_data, 1):
                question = question_data.get('question', {})
                user_answer = question_data.get('user_answer')
                
                # Get question from question bank (you'll need to implement this logic)
                # For now, we'll assume the question exists in the bank
                question_id = question.get('id')  # This should be the ID from question bank
                
                if not question_id:
                    logger.warning(f"No question ID found for question {i} in attempt {quiz_attempt_id}")
                    continue
                
                # Get the question from database to verify correct answer
                db_question = Question.query.get(question_id)
                if not db_question:
                    logger.warning(f"Question {question_id} not found in question bank")
                    continue
                
                # Determine if answer is correct
                is_correct = user_answer == db_question.correct_answer if user_answer is not None else False
                
                detail = QuizAttemptDetail(
                    quiz_attempt_id=quiz_attempt_id,
                    question_id=question_id,
                    question_number=i,
                    user_answer=user_answer,
                    is_correct=is_correct
                )
                self.db.session.add(detail)
            
            logger.info(f"Recorded {len(questions_data)} question details for attempt {quiz_attempt_id}")
            
        except Exception as e:
            logger.error(f"Error recording quiz details for attempt {quiz_attempt_id}: {e}")
            raise
    
    def get_user_quiz_history(self, user_id, limit=10):
        """Get quiz history for a user"""
        try:
            return QuizAttempt.query.filter_by(user_id=user_id)\
                .order_by(QuizAttempt.created_at.desc())\
                .limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting quiz history for user {user_id}: {e}")
            return []
    
    def get_quiz_attempt_by_id(self, attempt_id):
        """Get a specific quiz attempt by ID"""
        try:
            return QuizAttempt.query.get(attempt_id)
        except Exception as e:
            logger.error(f"Error getting quiz attempt {attempt_id}: {e}")
            return None
    
    def get_quiz_attempt_details(self, attempt_id):
        """Get detailed data for a specific quiz attempt with full question data"""
        try:
            from ..models import QuizAttemptDetail
            details = QuizAttemptDetail.query.filter_by(quiz_attempt_id=attempt_id)\
                .order_by(QuizAttemptDetail.question_number).all()
            return [detail.to_dict_with_question() for detail in details]
        except Exception as e:
            logger.error(f"Error getting quiz attempt details {attempt_id}: {e}")
            return []
    
    def get_user_stats(self, user_id):
        """Get user statistics"""
        try:
            attempts = QuizAttempt.query.filter_by(user_id=user_id).all()
            if not attempts:
                return {
                    'total_attempts': 0,
                    'average_score': 0,
                    'best_score': 0,
                    'pro_attempts': 0,
                    'free_attempts': 0
                }
            
            total_attempts = len(attempts)
            average_score = sum(attempt.percentage for attempt in attempts) / total_attempts
            best_score = max(attempt.percentage for attempt in attempts)
            pro_attempts = len([a for a in attempts if a.is_pro_quiz])
            free_attempts = total_attempts - pro_attempts
            
            return {
                'total_attempts': total_attempts,
                'average_score': round(average_score, 1),
                'best_score': round(best_score, 1),
                'pro_attempts': pro_attempts,
                'free_attempts': free_attempts
            }
        except Exception as e:
            logger.error(f"Error getting user stats for user {user_id}: {e}")
            return None
    
    def check_pro_access(self, user_id):
        """Check if user has PRO access"""
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False
            
            if not user.is_pro:
                return False
            
            # Check if user has active subscription
            active_subscription = self.get_active_subscription(user_id)
            if not active_subscription:
                # If no active subscription, check if user was upgraded manually
                return user.is_pro
            
            return True
        except Exception as e:
            logger.error(f"Error checking PRO access for user {user_id}: {e}")
            return False
    
    # Question Bank Management Methods
    def get_questions_by_difficulty(self, difficulty_level, limit=None):
        """Get questions by difficulty level"""
        try:
            from ..models import Question
            query = Question.query.filter_by(
                difficulty_level=difficulty_level,
                is_active=True
            )
            if limit:
                query = query.limit(limit)
            return query.all()
        except Exception as e:
            logger.error(f"Error getting questions by difficulty {difficulty_level}: {e}")
            return []
    
    def get_random_questions(self, count, difficulty_level=None, topic_category=None):
        """Get random questions for quiz generation"""
        try:
            from ..models import Question
            import random
            
            query = Question.query.filter_by(is_active=True)
            
            if difficulty_level:
                query = query.filter_by(difficulty_level=difficulty_level)
            
            if topic_category:
                query = query.filter_by(topic_category=topic_category)
            
            all_questions = query.all()
            
            if len(all_questions) <= count:
                return all_questions
            
            return random.sample(all_questions, count)
        except Exception as e:
            logger.error(f"Error getting random questions: {e}")
            return []
    
    def add_question_to_bank(self, question_text, options, correct_answer, explanation=None, 
                           difficulty_level=2, topic_category=None):
        """Add a new question to the question bank"""
        try:
            from ..models import Question
            
            question = Question(
                question_text=question_text,
                options=options,
                correct_answer=correct_answer,
                explanation=explanation,
                difficulty_level=difficulty_level,
                topic_category=topic_category
            )
            
            self.db.session.add(question)
            self.db.session.commit()
            
            logger.info(f"Added question {question.id} to question bank")
            return question
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Error adding question to bank: {e}")
            return None
    
    def get_question_by_id(self, question_id):
        """Get a specific question from the bank"""
        try:
            from ..models import Question
            return Question.query.get(question_id)
        except Exception as e:
            logger.error(f"Error getting question {question_id}: {e}")
            return None
