"""
Payment Service for Razorpay Integration
"""
import os
import logging
import razorpay
from flask import current_app
import time

logger = logging.getLogger(__name__)

class PaymentService:
    """Service for handling Razorpay payments"""
    
    def __init__(self):
        """Initialize Razorpay client"""
        try:
            self.client = razorpay.Client(
                auth=(current_app.config.get('RAZORPAY_KEY_ID'), 
                      current_app.config.get('RAZORPAY_KEY_SECRET'))
            )
            logger.info("Razorpay client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Razorpay client: {e}")
            self.client = None
    
    def create_order(self, amount, currency="INR", receipt_id=None):
        """Create a new payment order"""
        try:
            if not self.client:
                logger.error("Razorpay client not initialized")
                raise Exception("Payment service not configured properly")
            
            # Check if Razorpay keys are configured
            key_id = current_app.config.get('RAZORPAY_KEY_ID')
            key_secret = current_app.config.get('RAZORPAY_KEY_SECRET')
            
            if not key_id or key_id == 'your_razorpay_key_id_here':
                logger.error("Razorpay keys not configured")
                raise Exception("Payment service not configured")
            
            if not key_secret or key_secret == 'your_razorpay_key_secret_here':
                logger.error("Razorpay secret not configured")
                raise Exception("Payment service not configured")
            
            order_data = {
                'amount': amount * 100,  # Razorpay expects amount in paise
                'currency': currency,
                'receipt': receipt_id or f"receipt_{int(time.time())}",
                'notes': {
                    'description': 'dbt Certification Quiz Pro Upgrade'
                }
            }
            
            order = self.client.order.create(data=order_data)
            logger.info(f"Created Razorpay order: {order['id']}")
            return order
            
        except Exception as e:
            logger.error(f"Error creating Razorpay order: {e}")
            raise e
    
    def verify_payment(self, payment_id, order_id, signature):
        """Verify payment signature"""
        try:
            if not self.client:
                logger.error("Razorpay client not initialized")
                return False
            
            # Verify the payment signature
            params_dict = {
                'razorpay_payment_id': payment_id,
                'razorpay_order_id': order_id,
                'razorpay_signature': signature
            }
            
            self.client.utility.verify_payment_signature(params_dict)
            logger.info(f"Payment verified successfully: {payment_id}")
            return True
            
        except Exception as e:
            logger.error(f"Payment verification failed: {e}")
            return False
    
    def get_payment_details(self, payment_id):
        """Get payment details from Razorpay"""
        try:
            if not self.client:
                logger.error("Razorpay client not initialized")
                return None
            
            payment = self.client.payment.fetch(payment_id)
            logger.info(f"Retrieved payment details: {payment_id}")
            return payment
            
        except Exception as e:
            logger.error(f"Error fetching payment details: {e}")
            return None
    
    def refund_payment(self, payment_id, amount=None, reason="User requested refund"):
        """Refund a payment"""
        try:
            if not self.client:
                logger.error("Razorpay client not initialized")
                return None
            
            refund_data = {
                'reason': reason
            }
            
            if amount:
                refund_data['amount'] = amount * 100  # Convert to paise
            
            refund = self.client.payment.refund(payment_id, refund_data)
            logger.info(f"Refund created: {refund['id']}")
            return refund
            
        except Exception as e:
            logger.error(f"Error creating refund: {e}")
            return None
