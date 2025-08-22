"""
Quiz service for dbt Certification Quiz Application
"""
import time
import logging
from .scoring_service import ScoringService
from ..repo.markdown_repository import MarkdownQuestionRepository

logger = logging.getLogger(__name__)


class QuizService:
    """Service for managing quiz operations"""
    
    def __init__(self):
        """Initialize quiz service"""
        self.repository = MarkdownQuestionRepository()
        self.scoring_service = ScoringService()
        logger.info("Quiz service initialized")
    
    def get_quiz_config(self, num_questions, difficulty):
        """Get quiz configuration with questions from repository"""
        try:
            questions = self.repository.get_questions(num_questions, difficulty)
            
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
                "questions": questions
            }
            
            logger.info(f"Generated quiz config: {num_questions} questions, difficulty {difficulty}")
            return config
            
        except Exception as e:
            logger.error(f"Error generating quiz config: {e}")
            raise
    
    def get_question_stats(self):
        """Get statistics about available questions"""
        return self.repository.get_question_stats()
    
    def validate_answer(self, question_id, user_answer, correct_answer):
        """Validate user answer and return score"""
        return self.scoring_service.validate_answer(question_id, user_answer, correct_answer)
