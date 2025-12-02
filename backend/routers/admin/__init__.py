"""
Admin routes for dbt Certification Quiz Application
"""
import logging
from flask import Blueprint, render_template, request, jsonify, current_app, redirect, url_for
from backend.services.oauth_service import OAuthService
from backend.models import User, Question, db

# Create admin blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# Setup logging
logger = logging.getLogger(__name__)


@admin_bp.route('/users')
def admin_get_users():
    """Get all users for admin panel"""
    try:
        # Check if user is admin
        if not OAuthService.is_admin():
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get database service
        db_service = current_app.database_service
        
        # Get all users
        users = User.query.order_by(User.created_at.desc()).all()
        
        # Fix any data inconsistencies (sync is_pro with role)
        for user in users:
            if user.is_pro and user.role == 'regular':
                # User has PRO access but role is regular - sync it
                user.role = 'pro'
                logger.info(f"Fixed data inconsistency for user {user.id}: set role to 'pro' (is_pro was True)")
            elif not user.is_pro and user.role in ['pro', 'admin']:
                # User has pro/admin role but is_pro is False - sync it
                user.is_pro = True
                logger.info(f"Fixed data inconsistency for user {user.id}: set is_pro to True (role was {user.role})")
        
        # Commit any fixes
        if users:
            db_service.db.session.commit()
        
        users_data = []
        for user in users:
            users_data.append({
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'role': user.role,
                'is_pro': user.is_pro,
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'quiz_attempts_count': len(user.quiz_attempts) if hasattr(user, 'quiz_attempts') else 0
            })
        
        return jsonify({
            'success': True,
            'users': users_data,
            'total': len(users_data)
        })
        
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        return jsonify({'error': 'Failed to get users'}), 500


@admin_bp.route('/questions')
def admin_get_questions():
    """Get all questions for admin panel"""
    try:
        # Check if user is admin
        if not OAuthService.is_admin():
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get all questions
        questions = Question.query.order_by(Question.created_at.desc()).all()
        
        questions_data = []
        for question in questions:
            questions_data.append({
                'id': question.id,
                'question_id': question.question_id,
                'question_text': question.question_text[:100] + '...' if len(question.question_text) > 100 else question.question_text,
                'topic': question.topic_category,
                'difficulty': question.difficulty_level,
                'is_active': question.is_active,
                'is_pro_only': question.is_pro_only,
                'created_at': question.created_at.isoformat() if question.created_at else None
            })
        
        return jsonify({
            'success': True,
            'questions': questions_data,
            'total': len(questions_data),
            'regular': len([q for q in questions_data if not q['is_pro_only']]),
            'pro_only': len([q for q in questions_data if q['is_pro_only']])
        })
        
    except Exception as e:
        logger.error(f"Error getting questions: {e}")
        return jsonify({'error': 'Failed to get questions'}), 500


@admin_bp.route('/user/<int:user_id>/update-role', methods=['POST'])
def admin_update_user_role(user_id):
    """Update user role (admin only)"""
    try:
        # Check if user is admin
        if not OAuthService.is_admin():
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        new_role = data.get('role')
        
        if new_role not in ['regular', 'pro', 'admin']:
            return jsonify({'error': 'Invalid role'}), 400
        
        # Get database service
        db_service = current_app.database_service
        
        # Update user role
        user = db_service.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Update role and is_pro status
        user.role = new_role
        if new_role in ['pro', 'admin']:
            user.is_pro = True
        else:
            user.is_pro = False
        
        db_service.db.session.commit()
        
        logger.info(f"Admin updated user {user_id} role to {new_role}")
        
        return jsonify({
            'success': True,
            'message': f'User role updated to {new_role}'
        })
        
    except Exception as e:
        logger.error(f"Error updating user role: {e}")
        return jsonify({'error': 'Failed to update user role'}), 500


@admin_bp.route('/user/<int:user_id>/delete', methods=['DELETE', 'POST'])
def admin_delete_user(user_id):
    """Delete a user (admin only)"""
    try:
        # Check if user is admin
        if not OAuthService.is_admin():
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Prevent deleting yourself
        current_user = OAuthService.get_current_user()
        if current_user and current_user.get('id') == user_id:
            return jsonify({'error': 'You cannot delete your own account'}), 400
        
        # Get database service
        db_service = current_app.database_service
        
        # Get user to check if exists
        user = db_service.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Delete user
        success = db_service.delete_user(user_id)
        
        if success:
            logger.info(f"Admin deleted user {user_id}")
            return jsonify({
                'success': True,
                'message': 'User deleted successfully'
            })
        else:
            return jsonify({'error': 'Failed to delete user'}), 500
        
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        return jsonify({'error': 'Failed to delete user'}), 500


@admin_bp.route('/user/<int:user_id>/toggle-active', methods=['POST'])
def admin_toggle_user_active(user_id):
    """Toggle user active/inactive status (admin only)"""
    try:
        # Check if user is admin
        if not OAuthService.is_admin():
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Prevent deactivating yourself
        current_user = OAuthService.get_current_user()
        if current_user and current_user.get('id') == user_id:
            return jsonify({'error': 'You cannot deactivate your own account'}), 400
        
        # Get database service
        db_service = current_app.database_service
        
        # Get user
        user = db_service.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Toggle active status
        user.is_active = not user.is_active
        db_service.db.session.commit()
        
        status = 'activated' if user.is_active else 'deactivated'
        logger.info(f"Admin {status} user {user_id}")
        
        return jsonify({
            'success': True,
            'message': f'User {status} successfully',
            'is_active': user.is_active
        })
        
    except Exception as e:
        logger.error(f"Error toggling user active status: {e}")
        return jsonify({'error': 'Failed to toggle user status'}), 500


@admin_bp.route('/question/<int:question_id>/toggle-active', methods=['POST'])
def admin_toggle_question_active(question_id):
    """Toggle question active/inactive status (admin only)"""
    try:
        # Check if user is admin
        if not OAuthService.is_admin():
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get question
        question = Question.query.get(question_id)
        if not question:
            return jsonify({'error': 'Question not found'}), 404
        
        # Toggle active status
        question.is_active = not question.is_active
        db.session.commit()
        
        status = 'activated' if question.is_active else 'deactivated'
        logger.info(f"Admin {status} question {question_id}")
        
        return jsonify({
            'success': True,
            'message': f'Question {status} successfully',
            'is_active': question.is_active
        })
        
    except Exception as e:
        logger.error(f"Error toggling question active status: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to toggle question status'}), 500


@admin_bp.route('/question/<int:question_id>/update-type', methods=['POST'])
def admin_update_question_type(question_id):
    """Update question type (PRO-only/Regular) (admin only)"""
    try:
        # Check if user is admin
        if not OAuthService.is_admin():
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        is_pro_only = data.get('is_pro_only', False)
        
        if not isinstance(is_pro_only, bool):
            return jsonify({'error': 'Invalid type value'}), 400
        
        # Get question
        question = Question.query.get(question_id)
        if not question:
            return jsonify({'error': 'Question not found'}), 404
        
        # Update question type
        question.is_pro_only = is_pro_only
        db.session.commit()
        
        type_name = 'PRO-only' if is_pro_only else 'Regular'
        logger.info(f"Admin updated question {question_id} type to {type_name}")
        
        return jsonify({
            'success': True,
            'message': f'Question type updated to {type_name}',
            'is_pro_only': question.is_pro_only
        })
        
    except Exception as e:
        logger.error(f"Error updating question type: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to update question type'}), 500

