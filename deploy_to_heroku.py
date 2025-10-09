#!/usr/bin/env python3
"""
Simple Heroku Deployment Script
Run this after installing Heroku CLI
"""
import subprocess
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_command(command, description):
    """Run a command and show result"""
    print(f"\n🔄 {description}...")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Success!")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Failed!")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def check_heroku_cli():
    """Check if Heroku CLI is installed"""
    return run_command("heroku --version", "Checking Heroku CLI")

def deploy_to_heroku():
    """Deploy portfolio to Heroku"""
    print("🚀 Portfolio Heroku Deployment")
    print("=" * 50)
    
    # Check Heroku CLI
    if not check_heroku_cli():
        print("\n❌ Heroku CLI not found!")
        print("📥 Please install it from: https://devcenter.heroku.com/articles/heroku-cli")
        print("🔄 Then run this script again")
        return False
    
    # Check if logged in
    if not run_command("heroku auth:whoami", "Checking Heroku login"):
        print("\n🔐 Please login to Heroku first:")
        print("Run: heroku login")
        return False
    
    # Create app (you can change the name)
    app_name = "mahanth-portfolio"
    print(f"\n🏗️ Creating Heroku app: {app_name}")
    
    # Try to create app (might fail if name exists)
    create_result = subprocess.run(f"heroku create {app_name}", shell=True, capture_output=True, text=True)
    if "Name is already taken" in create_result.stderr:
        print(f"📱 App '{app_name}' already exists, using it...")
    elif create_result.returncode != 0:
        print("🎲 Creating app with random name...")
        if not run_command("heroku create", "Creating Heroku app"):
            return False
    else:
        print(f"✅ Created app: {app_name}")
    
    # Set environment variables
    print("\n🔧 Setting environment variables...")
    env_vars = {
        'FLASK_SECRET_KEY': os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-this'),
        'FLASK_ENV': 'production',
        'GMAIL_USERNAME': os.getenv('GMAIL_USERNAME'),
        'GMAIL_APP_PASSWORD': os.getenv('GMAIL_APP_PASSWORD'),
        'ADMIN_EMAIL': os.getenv('ADMIN_EMAIL')
    }
    
    for key, value in env_vars.items():
        if value:
            command = f'heroku config:set {key}="{value}"'
            run_command(command, f"Setting {key}")
        else:
            print(f"⚠️ Warning: {key} not found in .env file")
    
    # Commit any pending changes
    print("\n📝 Committing any pending changes...")
    run_command("git add .", "Adding files to git")
    run_command('git commit -m "Prepare for Heroku deployment"', "Committing changes")
    
    # Deploy to Heroku
    print("\n🚀 Deploying to Heroku...")
    if run_command("git push heroku main", "Pushing to Heroku"):
        print("\n🎉 Deployment successful!")
        
        # Open the app
        print("\n🌐 Opening your live website...")
        run_command("heroku open", "Opening app in browser")
        
        # Show app info
        print("\n📊 App Information:")
        run_command("heroku apps:info", "Getting app info")
        
        return True
    else:
        print("\n❌ Deployment failed!")
        print("📋 Check logs with: heroku logs --tail")
        return False

if __name__ == "__main__":
    success = deploy_to_heroku()
    
    if success:
        print("\n🎉 Your portfolio is now live on Heroku!")
        print("📋 Useful commands:")
        print("   heroku logs --tail    # View logs")
        print("   heroku restart        # Restart app")
        print("   heroku open           # Open in browser")
    else:
        print("\n❌ Deployment failed. Check the errors above.")
    
    input("\nPress Enter to exit...")