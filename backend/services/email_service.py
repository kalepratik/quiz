import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending emails via SMTP"""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.from_email = os.getenv('FROM_EMAIL', self.smtp_username)
        self.from_name = os.getenv('FROM_NAME', 'dbt Quiz Support')
        self.to_email = os.getenv('TO_EMAIL')  # Your email address
        
    def send_contact_form_email(self, name: str, email: str, subject: str, message: str) -> bool:
        """
        Send contact form email to the admin
        
        Args:
            name: Sender's name
            email: Sender's email
            subject: Email subject
            message: Email message
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            if not all([self.smtp_username, self.smtp_password, self.to_email]):
                logger.error("Email configuration missing. Please set SMTP_USERNAME, SMTP_PASSWORD, and TO_EMAIL environment variables.")
                return False
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = formataddr((self.from_name, self.from_email))
            msg['To'] = self.to_email
            msg['Subject'] = f"Contact Form: {subject}"
            
            # Create HTML body
            html_body = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px 8px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 20px; border-radius: 0 0 8px 8px; }}
                    .field {{ margin-bottom: 15px; }}
                    .label {{ font-weight: bold; color: #555; }}
                    .value {{ margin-top: 5px; padding: 10px; background: white; border-radius: 4px; border-left: 4px solid #667eea; }}
                    .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>New Contact Form Submission</h2>
                        <p>You have received a new message from the dbt Quiz contact form.</p>
                    </div>
                    
                    <div class="content">
                        <div class="field">
                            <div class="label">Name:</div>
                            <div class="value">{name}</div>
                        </div>
                        
                        <div class="field">
                            <div class="label">Email:</div>
                            <div class="value">{email}</div>
                        </div>
                        
                        <div class="field">
                            <div class="label">Subject:</div>
                            <div class="value">{subject}</div>
                        </div>
                        
                        <div class="field">
                            <div class="label">Message:</div>
                            <div class="value">{message.replace(chr(10), '<br>')}</div>
                        </div>
                        
                        <div class="footer">
                            <p>This email was sent from the contact form on your dbt Quiz website.</p>
                            <p>To reply to this person, use their email address: {email}</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
                
            logger.info(f"Contact form email sent successfully from {email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send contact form email: {str(e)}")
            return False
    
    def send_auto_reply(self, to_email: str, name: str) -> bool:
        """
        Send auto-reply email to the person who submitted the contact form
        
        Args:
            to_email: Recipient email
            name: Recipient name
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            if not all([self.smtp_username, self.smtp_password]):
                logger.error("Email configuration missing for auto-reply.")
                return False
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = formataddr((self.from_name, self.from_email))
            msg['To'] = to_email
            msg['Subject'] = "Thank you for contacting us - dbt Quiz"
            
            # Create HTML body
            html_body = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px 8px 0 0; text-align: center; }}
                    .content {{ background: #f9f9f9; padding: 20px; border-radius: 0 0 8px 8px; }}
                    .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666; text-align: center; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>Thank you for contacting us!</h2>
                    </div>
                    
                    <div class="content">
                        <p>Dear {name},</p>
                        
                        <p>Thank you for reaching out to us. We have received your message and will get back to you as soon as possible, typically within 24-48 hours.</p>
                        
                        <p>In the meantime, if you have any urgent questions about our dbt certification quiz, you can:</p>
                        
                        <ul>
                            <li>Check our <a href="/legal">Legal Information</a> page for common questions</li>
                            <li>Review our quiz features and pricing</li>
                            <li>Explore our comprehensive dbt practice questions</li>
                        </ul>
                        
                        <p>We appreciate your interest in our dbt certification preparation platform!</p>
                        
                        <p>Best regards,<br>
                        The dbt Quiz Team</p>
                        
                        <div class="footer">
                            <p>This is an automated response. Please do not reply to this email.</p>
                            <p>If you need immediate assistance, please visit our website.</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
                
            logger.info(f"Auto-reply email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send auto-reply email: {str(e)}")
            return False
