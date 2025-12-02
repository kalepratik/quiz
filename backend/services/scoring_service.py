"""
Scoring service for dbt Certification Quiz Application
"""
import logging

logger = logging.getLogger(__name__)


class ScoringService:
    """Service for scoring and validating quiz answers"""
    
    def __init__(self):
        """Initialize scoring service"""
        logger.info("Scoring service initialized")
    
    def validate_answer(self, question_id, user_answer, correct_answer):
        """Validate user answer and return score"""
        try:
            is_correct = user_answer == correct_answer
            score = 1 if is_correct else 0
            
            logger.debug(f"Question {question_id}: User answer {user_answer}, "
                        f"Correct answer {correct_answer}, Score {score}")
            
            return {
                'question_id': question_id,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'score': score
            }
            
        except Exception as e:
            logger.error(f"Error validating answer for question {question_id}: {e}")
            raise
    
    def calculate_total_score(self, answers):
        """Calculate total score from list of answer results"""
        try:
            total_score = sum(answer['score'] for answer in answers)
            total_questions = len(answers)
            percentage = (total_score / total_questions * 100) if total_questions > 0 else 0
            
            return {
                'total_score': total_score,
                'total_questions': total_questions,
                'percentage': round(percentage, 1),
                'answers': answers
            }
            
        except Exception as e:
            logger.error(f"Error calculating total score: {e}")
            raise
