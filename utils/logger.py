import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logging(app=None, log_level=logging.INFO):
    """
    Setup comprehensive logging for the Flask application
    """
    # Create logs directory if it doesn't exist
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    )
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # File handler for all logs
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'portfolio.log'),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(file_handler)
    
    # File handler for errors only
    error_handler = RotatingFileHandler(
        os.path.join(log_dir, 'errors.log'),
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(error_handler)
    
    # Console handler for development
    if app and app.debug:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(simple_formatter)
        root_logger.addHandler(console_handler)
    
    # Setup Flask app logging if app is provided
    if app:
        app.logger.setLevel(log_level)
        
        # Add security logging
        security_handler = RotatingFileHandler(
            os.path.join(log_dir, 'security.log'),
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        security_handler.setLevel(logging.INFO)
        security_handler.setFormatter(detailed_formatter)
        
        security_logger = logging.getLogger('security')
        security_logger.addHandler(security_handler)
        
        # Add access logging
        access_handler = RotatingFileHandler(
            os.path.join(log_dir, 'access.log'),
            maxBytes=10485760,  # 10MB
            backupCount=10
        )
        access_handler.setLevel(logging.INFO)
        access_handler.setFormatter(simple_formatter)
        
        access_logger = logging.getLogger('access')
        access_logger.addHandler(access_handler)
    
    logging.info("Logging system initialized")
    return root_logger

def log_request(request, response_status=None):
    """Log HTTP requests"""
    access_logger = logging.getLogger('access')
    access_logger.info(
        f"{request.remote_addr} - {request.method} {request.path} - "
        f"Status: {response_status} - User-Agent: {request.headers.get('User-Agent', 'Unknown')}"
    )

def log_security_event(event_type, details, request=None):
    """Log security-related events"""
    security_logger = logging.getLogger('security')
    
    message = f"SECURITY EVENT: {event_type} - {details}"
    if request:
        message += f" - IP: {request.remote_addr} - User-Agent: {request.headers.get('User-Agent', 'Unknown')}"
    
    security_logger.warning(message)

def log_admin_action(action, user_ip, details=None):
    """Log admin panel actions"""
    security_logger = logging.getLogger('security')
    message = f"ADMIN ACTION: {action} - IP: {user_ip}"
    if details:
        message += f" - Details: {details}"
    security_logger.info(message)