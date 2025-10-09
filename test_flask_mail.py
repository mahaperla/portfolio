#!/usr/bin/env python3
"""
Flask-Mail Configuration Test
Tests Flask-Mail setup with current configuration
"""
import os
from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv

def test_flask_mail():
    print("🧪 Testing Flask-Mail Configuration...")
    
    # Load environment variables
    load_dotenv()
    
    # Create Flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test'
    
    # Mail configuration (matching your app.py)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False  # Important: TLS and SSL are mutually exclusive
    app.config['MAIL_USERNAME'] = os.getenv('GMAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('GMAIL_APP_PASSWORD')
    
    # Debug configuration
    print(f"📧 Mail Server: {app.config['MAIL_SERVER']}")
    print(f"📧 Mail Port: {app.config['MAIL_PORT']}")
    print(f"🔐 Use TLS: {app.config['MAIL_USE_TLS']}")
    print(f"🔐 Use SSL: {app.config.get('MAIL_USE_SSL', 'Not set')}")
    print(f"👤 Username: {app.config['MAIL_USERNAME']}")
    print(f"🔑 Password Length: {len(app.config['MAIL_PASSWORD']) if app.config['MAIL_PASSWORD'] else 0}")
    
    # Initialize mail
    mail = Mail(app)
    
    try:
        with app.app_context():
            print("\n🔄 Testing Flask-Mail...")
            
            # Create test message
            msg = Message(
                subject="Flask-Mail Test from Portfolio",
                sender=app.config['MAIL_USERNAME'],
                recipients=[os.getenv('ADMIN_EMAIL')]
            )
            
            msg.html = """
            <h3>Flask-Mail Test Email</h3>
            <p>This email was sent using Flask-Mail configuration.</p>
            <p>If you receive this, Flask-Mail is working correctly!</p>
            """
            
            print("📤 Sending test email via Flask-Mail...")
            mail.send(msg)
            
            print("✅ Flask-Mail test successful!")
            return True
            
    except Exception as e:
        print(f"❌ Flask-Mail Error: {str(e)}")
        print("🔍 Error Type:", type(e).__name__)
        
        # Common error diagnoses
        if "Authentication" in str(e):
            print("   - Check Gmail App Password")
        elif "Connection" in str(e):
            print("   - Check network/firewall settings")
        elif "SSL" in str(e) or "TLS" in str(e):
            print("   - Check TLS/SSL configuration")
        
        return False

if __name__ == "__main__":
    print("🔒 Flask-Mail Configuration Test")
    print("=" * 50)
    
    success = test_flask_mail()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Flask-Mail is configured correctly!")
    else:
        print("❌ Flask-Mail configuration needs fixing.")