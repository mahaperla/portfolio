#!/usr/bin/env python3
"""
Properly Initialize Security System
This script properly initializes the security system and generates a working admin password
"""
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables
load_dotenv()

try:
    from utils.security import get_security_manager, init_security_system
    
    def fix_admin_password():
        print("🔧 Fixing Admin Password System...")
        
        # Initialize the security system properly
        print("🔄 Initializing security system...")
        if init_security_system():
            print("✅ Security system initialized successfully!")
            
            # Get the security manager
            security_manager = get_security_manager()
            
            # Read the current password from the file
            try:
                with open('temp_dev_password.txt', 'r') as f:
                    content = f.read()
                    for line in content.split('\n'):
                        if 'Development Admin Password:' in line:
                            current_password = line.split(': ')[1].strip()
                            print(f"📄 Found password in file: {current_password}")
                            break
                    else:
                        print("❌ Could not find password in file")
                        return False
                        
                # Test the current password
                print("🧪 Testing current password...")
                if security_manager.validate_admin_access(current_password):
                    print("✅ Current password is valid!")
                    print(f"🔑 Admin Password: {current_password}")
                    print(f"🔗 Admin URL: http://localhost:5000/admin/login")
                    return True
                else:
                    print("❌ Current password is invalid/expired")
                    print("🔄 The system should have generated a new one during initialization")
                    
                    # Check if a new password was created
                    try:
                        with open('temp_dev_password.txt', 'r') as f:
                            new_content = f.read()
                            if new_content != content:
                                print("📄 New password file detected!")
                                for line in new_content.split('\n'):
                                    if 'Development Admin Password:' in line:
                                        new_password = line.split(': ')[1].strip()
                                        print(f"🔑 New Admin Password: {new_password}")
                                        print(f"🔗 Admin URL: http://localhost:5000/admin/login")
                                        return True
                    except:
                        pass
                    
                    return False
                    
            except FileNotFoundError:
                print("❌ Password file not found!")
                return False
                
        else:
            print("❌ Failed to initialize security system")
            return False
    
    if __name__ == "__main__":
        print("🔒 Admin Password System Fix")
        print("=" * 50)
        
        success = fix_admin_password()
        
        print("\n" + "=" * 50)
        if success:
            print("🎉 Admin password system is working!")
            print("💡 You can now login to the admin panel")
        else:
            print("❌ Admin password system still has issues")
            print("💡 Try restarting the Flask app: python app.py")
            
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the app directory.")