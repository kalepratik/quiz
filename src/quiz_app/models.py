"""
Database models for dbt Certification Quiz Application
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


class User(db.Model):
    """User model for storing user information"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    google_id = db.Column(db.String(100), unique=True, nullable=True, index=True)
    profile_picture = db.Column(db.String(500), nullable=True)
    is_pro = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationship with subscriptions
    subscriptions = db.relationship('Subscription', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'google_id': self.google_id,
            'profile_picture': self.profile_picture,
            'is_pro': self.is_pro,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Subscription(db.Model):
    """Subscription model for tracking PRO subscriptions"""
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    razorpay_payment_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    razorpay_order_id = db.Column(db.String(100), nullable=False, index=True)
    amount = db.Column(db.Integer, nullable=False)  # Amount in paise
    currency = db.Column(db.String(3), default='INR', nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, completed, failed, cancelled
    payment_method = db.Column(db.String(50), nullable=True)
    subscription_start = db.Column(db.DateTime, nullable=True)
    subscription_end = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f'<Subscription {self.razorpay_payment_id}>'
    
    def to_dict(self):
        """Convert subscription to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'razorpay_payment_id': self.razorpay_payment_id,
            'razorpay_order_id': self.razorpay_order_id,
            'amount': self.amount,
            'currency': self.currency,
            'status': self.status,
            'payment_method': self.payment_method,
            'subscription_start': self.subscription_start.isoformat() if self.subscription_start else None,
            'subscription_end': self.subscription_end.isoformat() if self.subscription_end else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class QuizAttempt(db.Model):
    """Quiz attempt model for tracking user quiz attempts"""
    __tablename__ = 'quiz_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    question_count = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    correct_answers = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    is_pro_quiz = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    
    # Relationship with user
    user = db.relationship('User', backref='quiz_attempts')
    
    def __repr__(self):
        return f'<QuizAttempt {self.id} - User {self.user_id}>'
    
    def to_dict(self):
        """Convert quiz attempt to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_count': self.question_count,
            'difficulty': self.difficulty,
            'correct_answers': self.correct_answers,
            'total_questions': self.total_questions,
            'percentage': self.percentage,
            'is_pro_quiz': self.is_pro_quiz,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Question(db.Model):
    """Question bank model for storing all quiz questions"""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, unique=True, nullable=False)  # ID from markdown file (1-35)
    question_text = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON, nullable=False)  # Array of answer options
    correct_answer = db.Column(db.Integer, nullable=False)  # 0-based index (0=A, 1=B, 2=C, 3=D)
    explanation = db.Column(db.Text, nullable=True)
    difficulty_level = db.Column(db.Integer, default=2, nullable=False)  # 1=Easy, 2=Medium, 3=Hard
    topic_category = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f'<Question {self.id} - {self.topic_category}>'
    
    def to_dict(self):
        """Convert question to dictionary"""
        return {
            'id': self.id,
            'question_text': self.question_text,
            'options': self.options,
            'correct_answer': self.correct_answer,
            'explanation': self.explanation,
            'difficulty_level': self.difficulty_level,
            'topic_category': self.topic_category,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class QuizAttemptDetail(db.Model):
    """Minimal storage for individual question responses"""
    __tablename__ = 'quiz_attempt_details'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_attempt_id = db.Column(db.Integer, db.ForeignKey('quiz_attempts.id'), nullable=False, index=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False, index=True)
    question_number = db.Column(db.Integer, nullable=False)  # 1-based question number in the attempt
    user_answer = db.Column(db.Integer, nullable=True)  # 0-based index (0=A, 1=B, 2=C, 3=D), NULL if not answered
    is_correct = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    
    # Relationships
    quiz_attempt = db.relationship('QuizAttempt', backref='details')
    question = db.relationship('Question', backref='attempt_details')
    
    def __repr__(self):
        return f'<QuizAttemptDetail {self.id} - Attempt {self.quiz_attempt_id} - Q{self.question_number}>'
    
    def to_dict(self):
        """Convert quiz attempt detail to dictionary"""
        return {
            'id': self.id,
            'quiz_attempt_id': self.quiz_attempt_id,
            'question_id': self.question_id,
            'question_number': self.question_number,
            'user_answer': self.user_answer,
            'is_correct': self.is_correct,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def to_dict_with_question(self):
        """Convert to dictionary with full question data"""
        detail_dict = self.to_dict()
        if self.question:
            detail_dict.update({
                'question_text': self.question.question_text,
                'options': self.question.options,
                'correct_answer': self.question.correct_answer,
                'explanation': self.question.explanation,
                'difficulty_level': self.question.difficulty_level,
                'topic_category': self.question.topic_category
            })
        return detail_dict
