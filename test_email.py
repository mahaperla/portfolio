#!/usr/bin/env python3
"""
Email Configuration Test Script
Tests Gmail SMTP connection with App Password
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

def test_email_connection():
    print("🧪 Testing Email Configuration...")
    
    # Load environment variables
    load_dotenv()
    
    # Get email configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv('GMAIL_USERNAME')
    sender_password = os.getenv('GMAIL_APP_PASSWORD')
    recipient_email = os.getenv('ADMIN_EMAIL')
    
    print(f"📧 Sender Email: {sender_email}")
    print(f"📧 Recipient Email: {recipient_email}")
    print(f"🔑 Password Length: {len(sender_password) if sender_password else 0} characters")
    print(f"🔑 Password Format: {'✅ Correct (16 chars)' if sender_password and len(sender_password) == 16 else '❌ Incorrect'}")
    
    if not all([sender_email, sender_password, recipient_email]):
        print("❌ Missing email configuration!")
        print(f"   - Gmail Username: {'✅' if sender_email else '❌'}")
        print(f"   - Gmail Password: {'✅' if sender_password else '❌'}")
        print(f"   - Admin Email: {'✅' if recipient_email else '❌'}")
        return False
    
    try:
        print("\n🔄 Testing SMTP Connection...")
        
        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = "Portfolio Email Test"
        
        body = """
        This is a test email from your portfolio website.
        
        If you receive this email, your Gmail App Password is working correctly!
        
        Test Details:
        - SMTP Server: smtp.gmail.com
        - Port: 587
        - TLS: Enabled
        - Authentication: App Password
        """
        
        message.attach(MIMEText(body, "plain"))
        
        # Connect to server
        print("📡 Connecting to Gmail SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        
        print("🔐 Starting TLS encryption...")
        server.starttls()
        
        print("🔑 Authenticating with Gmail...")
        server.login(sender_email, sender_password)
        
        print("📤 Sending test email...")
        text = message.as_string()
        server.sendmail(sender_email, recipient_email, text)
        
        print("✅ Email sent successfully!")
        print(f"📬 Check your inbox: {recipient_email}")
        
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication Error: {e}")
        print("🔍 Possible issues:")
        print("   - Incorrect Gmail App Password")
        print("   - 2-Factor Authentication not enabled")
        print("   - App Password not generated correctly")
        return False
        
    except smtplib.SMTPException as e:
        print(f"❌ SMTP Error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    print("🔒 Portfolio Email Test")
    print("=" * 50)
    
    success = test_email_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Email configuration is working!")
        print("Your portfolio contact form should now work correctly.")
    else:
        print("❌ Email configuration needs fixing.")
        print("Please check the error messages above.")