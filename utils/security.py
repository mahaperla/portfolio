import os
import secrets
import string
import hashlib
import smtplib
import json
import logging
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import schedule
import time

class SecurityManager:
    def __init__(self, settings_file='settings.json'):
        self.app_dir = os.path.dirname(os.path.dirname(__file__))
        self.settings_file = os.path.join(self.app_dir, settings_file)
        self.password_file = 'temp_admin_password.txt'
        self.logger = logging.getLogger(__name__)
        self.load_settings()
        self.current_password_hash = None
        self.password_generated_at = None
        
    def load_settings(self):
        """Load settings from JSON file"""
        try:
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            self.logger.error(f"Settings file {self.settings_file} not found")
            raise
    
    def generate_password(self, length=12):
        """Generate a secure random password"""
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        """Verify password against stored hash"""
        if not self.current_password_hash:
            return False
        return self.hash_password(password) == self.current_password_hash
    
    def send_password_email(self, password):
        """Send password via email using Gmail SMTP"""
        try:
            # Get email settings from environment variables
            sender_email = os.getenv('GMAIL_USERNAME')
            sender_password = os.getenv('GMAIL_APP_PASSWORD')
            recipient_email = os.getenv('ADMIN_EMAIL')
            
            if not all([sender_email, sender_password, recipient_email]):
                self.logger.error("Email credentials not found in environment variables")
                return False
            
            # Create message
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = "Portfolio Admin - New Temporary Password"
            
            # Email body
            body = f"""
            <html>
            <body>
                <h2>Portfolio Admin Access</h2>
                <p>Your new temporary admin password has been generated:</p>
                <p><strong style="font-size: 18px; color: #007bff;">{password}</strong></p>
                <p>This password will expire in {self.settings['security']['password_reset_interval_minutes']} minutes.</p>
                <p>Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <hr>
                <p><em>This is an automated message from your Portfolio Admin System.</em></p>
            </body>
            </html>
            """
            
            message.attach(MIMEText(body, "html"))
            
            # Send email
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, message.as_string())
            
            self.logger.info("Password email sent successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send password email: {str(e)}")
            return False
    
    def generate_and_send_password(self):
        """Generate new password, hash it, and send via email"""
        try:
            # Generate new password
            new_password = self.generate_password()
            self.current_password_hash = self.hash_password(new_password)
            self.password_generated_at = datetime.now()
            
            # Send email
            if self.send_password_email(new_password):
                self.logger.info("New admin password generated and sent")
                return True
            else:
                self.logger.error("Failed to send password email")
                return False
                
        except Exception as e:
            self.logger.error(f"Error generating password: {str(e)}")
            return False
    
    def is_password_expired(self):
        """Check if current password has expired"""
        if not self.password_generated_at:
            return True
            
        expiry_time = self.password_generated_at + timedelta(
            minutes=self.settings['security']['password_reset_interval_minutes']
        )
        return datetime.now() > expiry_time
    
    def schedule_password_reset(self):
        """Schedule automatic password reset"""
        interval = self.settings['security']['password_reset_interval_minutes']
        schedule.every(interval).minutes.do(self.generate_and_send_password)
        
        # Run scheduler in background thread
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        self.logger.info(f"Password reset scheduled every {interval} minutes")
    
    def initialize_security(self):
        """Initialize security system on app startup"""
        self.logger.info("Initializing security system...")
        
        # Check if we're in development mode
        if os.getenv('FLASK_ENV') == 'development':
            # In development, create a simple password for testing
            self.logger.warning("DEVELOPMENT MODE: Using simple password for testing")
            test_password = "admin123"
            self.current_password_hash = self.hash_password(test_password)
            self.password_generated_at = datetime.now()
            
            self.logger.warning(f"DEVELOPMENT PASSWORD: {test_password}")
            self.logger.warning("This password will work for the entire session")
            
            # Don't schedule resets in development mode
            self.logger.info("Security system initialized in development mode")
            return True
        
        # Production mode - generate and email password
        if self.generate_and_send_password():
            # Schedule automatic resets
            self.schedule_password_reset()
            self.logger.info("Security system initialized successfully")
            return True
        else:
            self.logger.error("Failed to initialize security system")
            return False
    
    def validate_admin_access(self, password):
        """Validate admin access with current password"""
        if self.is_password_expired():
            self.logger.warning("Admin access attempted with expired password")
            return False
            
        if self.verify_password(password):
            self.logger.info("Admin access granted")
            return True
        else:
            self.logger.warning("Admin access denied - invalid password")
            return False

# Global security manager instance
security_manager = None

def get_security_manager():
    """Get the global security manager instance"""
    global security_manager
    if security_manager is None:
        security_manager = SecurityManager()
    return security_manager

def init_security_system():
    """Initialize the security system"""
    manager = get_security_manager()
    return manager.initialize_security()