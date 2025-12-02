"""
Tests for repository layer
"""
import pytest
from src.quiz_app.repo.markdown_repository import MarkdownQuestionRepository


@pytest.fixture
def repo():
    """Create repository for testing"""
    return MarkdownQuestionRepository()


def test_repository_initialization(repo):
    """Test repository initialization"""
    assert repo is not None
    assert hasattr(repo, 'questions')


def test_get_question_stats(repo):
    """Test getting question statistics"""
    stats = repo.get_question_stats()
    
    assert 'total' in stats
    assert 'easy' in stats
    assert 'medium' in stats
    assert 'difficulty' in stats
    assert 'critical' in stats
    
    # Ensure total is sum of all difficulties
    total = stats['easy'] + stats['medium'] + stats['difficulty'] + stats['critical']
    assert stats['total'] == total


def test_get_questions_default(repo):
    """Test getting questions with default parameters"""
    questions = repo.get_questions(5, 2)  # 5 questions, medium difficulty
    
    assert len(questions) <= 5
    assert all('id' in q for q in questions)
    assert all('question' in q for q in questions)
    assert all('options' in q for q in questions)
    assert all('correctAnswer' in q for q in questions)


def test_get_questions_no_preference(repo):
    """Test getting questions with no preference (mixed)"""
    questions = repo.get_questions(10, 0)  # 10 questions, no preference
    
    assert len(questions) <= 10
    assert all('id' in q for q in questions)
