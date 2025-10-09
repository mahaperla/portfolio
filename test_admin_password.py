#!/usr/bin/env python3
"""
Admin Password Test Script
Tests if the current admin password works with the security system
"""
import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables
load_dotenv()

try:
    from utils.security import get_security_manager
    
    def test_admin_password():
        print("🔐 Testing Admin Password System...")
        
        # Read the current password from file
        try:
            with open('temp_dev_password.txt', 'r') as f:
                content = f.read()
                print(f"📄 Password file content:\n{content}")
                
                # Extract password from the file
                for line in content.split('\n'):
                    if 'Development Admin Password:' in line:
                        password = line.split(': ')[1].strip()
                        print(f"🔑 Extracted password: {password}")
                        break
                else:
                    print("❌ Could not extract password from file")
                    return False
        except FileNotFoundError:
            print("❌ Password file not found!")
            return False
        
        # Test the security manager
        try:
            print("\n🔧 Initializing security manager...")
            security_manager = get_security_manager()
            
            print("🧪 Testing password validation...")
            is_valid = security_manager.validate_admin_access(password)
            
            if is_valid:
                print("✅ Password is VALID! You can use this to login to admin panel.")
                print(f"🔗 Admin URL: http://localhost:5000/admin/login")
                print(f"🔑 Password: {password}")
                return True
            else:
                print("❌ Password is INVALID or expired.")
                print("🔄 Generating new password...")
                
                # Try to generate a new password
                new_password = security_manager.generate_new_password()
                if new_password:
                    print(f"✅ New password generated: {new_password}")
                    return True
                else:
                    print("❌ Failed to generate new password")
                    return False
                    
        except Exception as e:
            print(f"❌ Security manager error: {e}")
            return False
    
    if __name__ == "__main__":
        print("🔒 Admin Password Test")
        print("=" * 50)
        
        success = test_admin_password()
        
        print("\n" + "=" * 50)
        if success:
            print("🎉 Admin password system is working!")
        else:
            print("❌ Admin password system needs attention.")
            
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the app directory.")