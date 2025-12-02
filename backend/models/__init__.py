"""
Database models for dbt Certification Quiz Application
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models - they will use db from this module
from .user_models import User, Subscription
from .quiz_models import Question, QuizAttempt, QuizAttemptDetail

__all__ = ['db', 'User', 'Subscription', 'Question', 'QuizAttempt', 'QuizAttemptDetail']

