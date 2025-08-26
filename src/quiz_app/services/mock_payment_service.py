"""
Mock Payment Service for Development Testing
This service simulates payment processing without requiring real Razorpay integration
"""
import logging
import time
import random

logger = logging.getLogger(__name__)

class MockPaymentService:
    """Mock service for testing payments without Razorpay"""
    
    def __init__(self):
        """Initialize mock payment service"""
        logger.info("Mock payment service initialized for development testing")
    
    def create_order(self, amount, currency="INR", receipt_id=None):
        """Create a mock payment order"""
        try:
            order_id = f"mock_order_{int(time.time())}_{random.randint(1000, 9999)}"
            
            mock_order = {
                'id': order_id,
                'amount': amount * 100,  # Convert to paise
                'currency': currency,
                'receipt': receipt_id or f"mock_receipt_{int(time.time())}",
                'status': 'created'
            }
            
            logger.info(f"Created mock order: {order_id}")
            return mock_order
            
        except Exception as e:
            logger.error(f"Error creating mock order: {e}")
            raise e
    
    def verify_payment(self, payment_id, order_id, signature):
        """Verify mock payment (always returns True for testing)"""
        try:
            # Simulate payment verification
            logger.info(f"Mock payment verification: {payment_id}")
            
            # For testing, we'll accept any payment with a valid format
            if payment_id and order_id and signature:
                logger.info("Mock payment verified successfully")
                return True
            else:
                logger.warning("Mock payment verification failed - missing parameters")
                return False
                
        except Exception as e:
            logger.error(f"Mock payment verification error: {e}")
            return False
    
    def get_payment_details(self, payment_id):
        """Get mock payment details"""
        try:
            mock_payment = {
                'id': payment_id,
                'status': 'captured',
                'amount': 30000,  # ₹300 in paise
                'currency': 'INR',
                'method': 'card',
                'card_id': 'mock_card_id',
                'bank': 'mock_bank',
                'wallet': None,
                'vpa': None,
                'email': 'test@example.com',
                'contact': '+919999999999',
                'fee': 0,
                'tax': 0,
                'error_code': None,
                'error_description': None,
                'created_at': int(time.time())
            }
            
            logger.info(f"Retrieved mock payment details: {payment_id}")
            return mock_payment
            
        except Exception as e:
            logger.error(f"Error fetching mock payment details: {e}")
            return None
