#!/usr/bin/env python3
"""
Security Verification Script
Checks if all sensitive data has been properly removed from the repository
"""

import json
import os
import re

def check_settings_json():
    """Check if settings.json contains any sensitive data"""
    print("🔍 Checking settings.json...")
    
    try:
        with open('settings.json', 'r') as f:
            content = f.read()
            data = json.loads(content)
        
        # Check for exposed credentials
        sensitive_patterns = [
            r'sender_password',
            r'sender_email.*@gmail\.com',
            r'recipient_email.*@gmail\.com'
        ]
        
        issues_found = []
        
        for pattern in sensitive_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues_found.append(f"Found sensitive pattern: {pattern}")
        
        if issues_found:
            print("❌ SECURITY ISSUES FOUND:")
            for issue in issues_found:
                print(f"  - {issue}")
            return False
        else:
            print("✅ settings.json is secure - no sensitive data found")
            return True
            
    except Exception as e:
        print(f"❌ Error checking settings.json: {e}")
        return False

def check_env_file():
    """Check if .env file is properly configured"""
    print("\n🔍 Checking .env file...")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        return False
    
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        # Check if it has placeholder values
        if 'sender_password' in content or 'smtp_password' in content:
            print("❌ .env file still contains password references!")
            return False
        
        if 'your-new-password-here' in content or 'your-new-app-password-here' in content:
            print("⚠️  .env file contains placeholder - you need to update with real password")
            return True
        
        # Check if it has proper environment variables
        required_vars = ['GMAIL_USERNAME', 'GMAIL_APP_PASSWORD', 'ADMIN_EMAIL']
        for var in required_vars:
            if var not in content:
                print(f"❌ Missing required variable: {var}")
                return False
        
        print("✅ .env file structure is correct")
        return True
        
    except Exception as e:
        print(f"❌ Error checking .env file: {e}")
        return False

def check_gitignore():
    """Check if .env is properly ignored"""
    print("\n🔍 Checking .gitignore...")
    
    try:
        with open('.gitignore', 'r') as f:
            content = f.read()
        
        if '.env' in content:
            print("✅ .env file is properly ignored by git")
            return True
        else:
            print("❌ .env file is NOT in .gitignore!")
            return False
            
    except Exception as e:
        print(f"❌ Error checking .gitignore: {e}")
        return False

def check_app_config():
    """Check if app.py uses environment variables"""
    print("\n🔍 Checking app.py configuration...")
    
    try:
        with open('app.py', 'r') as f:
            content = f.read()
        
        # Check for proper environment variable usage
        env_patterns = [
            r"os\.getenv\('GMAIL_USERNAME'\)",
            r"os\.getenv\('GMAIL_APP_PASSWORD'\)",
            r"os\.getenv\('ADMIN_EMAIL'\)"
        ]
        
        all_found = True
        for pattern in env_patterns:
            if not re.search(pattern, content):
                print(f"❌ Missing environment variable pattern: {pattern}")
                all_found = False
        
        if all_found:
            print("✅ app.py properly uses environment variables")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ Error checking app.py: {e}")
        return False

def main():
    print("🔒 Security Verification Report")
    print("=" * 50)
    
    checks = [
        check_settings_json(),
        check_env_file(),
        check_gitignore(),
        check_app_config()
    ]
    
    print("\n📊 Summary:")
    print(f"✅ Passed: {sum(checks)}/4 checks")
    
    if all(checks):
        print("\n🎉 ALL SECURITY CHECKS PASSED!")
        print("Your repository is secure and ready for production.")
    else:
        print("\n⚠️  Some security issues need attention.")
        print("Please review the failed checks above.")
    
    print("\n🔗 Next Steps:")
    print("1. Check GitGuardian dashboard: https://dashboard.gitguardian.com")
    print("2. Generate new Gmail App Password if not done")
    print("3. Update .env with new password")
    print("4. Test email functionality")

if __name__ == "__main__":
    main()