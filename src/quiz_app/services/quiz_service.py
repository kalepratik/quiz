"""
Quiz service for dbt Certification Quiz Application
"""
import time
import logging
from flask import current_app
from .scoring_service import ScoringService

logger = logging.getLogger(__name__)


class QuizService:
    """Service for managing quiz operations"""
    
    def __init__(self):
        """Initialize quiz service"""
        self.scoring_service = ScoringService()
        logger.info("Quiz service initialized")
    
    def get_quiz_config(self, num_questions, difficulty):
        """Get quiz configuration with questions from question bank"""
        try:
            # Get database service
            db_service = current_app.database_service
            
            # Get random questions from question bank
            questions = db_service.get_random_questions(
                count=num_questions,
                difficulty_level=difficulty if difficulty > 0 else None
            )
            
            # Convert questions to the expected format
            formatted_questions = []
            for question in questions:
                formatted_question = {
                    'id': question.id,
                    'question': question.question_text,
                    'options': question.options,
                    'correctAnswer': question.correct_answer,
                    'explanation': question.explanation,
                    'difficulty': question.difficulty_level,
                    'topic': question.topic_category
                }
                formatted_questions.append(formatted_question)
            
            # Handle difficulty name for no preference case
            if difficulty == 0 or difficulty == 5:
                difficulty_name = "Mixed"
            else:
                difficulty_name = ["Easy", "Medium", "Difficult", "Critical"][difficulty - 1]
            
            config = {
                "numQuestions": num_questions,
                "difficulty": difficulty,
                "difficultyName": difficulty_name,
                "timestamp": time.time(),
                "questions": formatted_questions
            }
            
            logger.info(f"Generated quiz config: {num_questions} questions, difficulty {difficulty}")
            return config
            
        except Exception as e:
            logger.error(f"Error generating quiz config: {e}")
            raise
    
    def get_question_stats(self):
        """Get statistics about available questions from question bank"""
        try:
            from ..models import Question, db
            from sqlalchemy import func
            
            # Get total questions
            total_questions = Question.query.filter_by(is_active=True).count()
            
            # Get questions by difficulty
            difficulty_stats = db.session.query(
                Question.difficulty_level,
                func.count(Question.id)
            ).filter_by(is_active=True).group_by(Question.difficulty_level).all()
            
            # Get questions by topic
            topic_stats = db.session.query(
                Question.topic_category,
                func.count(Question.id)
            ).filter_by(is_active=True).group_by(Question.topic_category).all()
            
            return {
                'total_questions': total_questions,
                'by_difficulty': {f"Level {d}": c for d, c in difficulty_stats},
                'by_topic': {t or 'Uncategorized': c for t, c in topic_stats}
            }
            
        except Exception as e:
            logger.error(f"Error getting question stats: {e}")
            return {'total_questions': 0, 'by_difficulty': {}, 'by_topic': {}}
    
    def validate_answer(self, question_id, user_answer, correct_answer):
        """Validate user answer and return score"""
        return self.scoring_service.validate_answer(question_id, user_answer, correct_answer)
