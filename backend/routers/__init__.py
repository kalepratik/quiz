"""
Routers package - API route handlers
"""
from .main import ui_bp, api_bp
from .admin import admin_bp

__all__ = ['ui_bp', 'api_bp', 'admin_bp']

