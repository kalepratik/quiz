"""
Tests for Flask routes
"""
import pytest
from src.quiz_app import create_app


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


def test_index_route(client):
    """Test main index route"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Enhanced dbt Quiz' in response.data


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/healthz')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'dbt-certification-quiz'


def test_configure_quiz_api(client):
    """Test quiz configuration API"""
    response = client.get('/api/configure-quiz?num_questions=5&difficulty=2')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'questions' in data
    assert 'numQuestions' in data
    assert 'difficulty' in data


def test_configure_quiz_defaults(client):
    """Test quiz configuration with defaults"""
    response = client.get('/api/configure-quiz')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['numQuestions'] == 10  # Default
    assert data['difficulty'] == 2     # Default
