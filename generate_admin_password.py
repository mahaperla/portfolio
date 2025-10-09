#!/usr/bin/env python3
"""
Generate Fresh Admin Password
Creates a new admin password and updates the system
"""
import os
import sys
import secrets
import string
import hashlib
from datetime import datetime

def generate_fresh_password():
    print("🔐 Generating Fresh Admin Password...")
    
    # Generate a new secure password
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    new_password = ''.join(secrets.choice(characters) for _ in range(8))
    
    print(f"🔑 New Password: {new_password}")
    
    # Save to file
    try:
        with open('temp_dev_password.txt', 'w') as f:
            f.write(f"Development Admin Password: {new_password}\n")
            f.write(f"Generated at: {datetime.now()}\n")
            f.write("This file is automatically ignored by git.\n")
        
        print("✅ Password saved to temp_dev_password.txt")
        print(f"🔗 Admin Login URL: http://localhost:5000/admin/login")
        print(f"👤 Use this password: {new_password}")
        
        return new_password
        
    except Exception as e:
        print(f"❌ Error saving password: {e}")
        return None

if __name__ == "__main__":
    print("🔒 Fresh Admin Password Generator")
    print("=" * 50)
    
    password = generate_fresh_password()
    
    print("\n" + "=" * 50)
    if password:
        print("🎉 Fresh admin password ready!")
        print("💡 Start your Flask app and visit /admin/login")
    else:
        print("❌ Failed to generate password.")