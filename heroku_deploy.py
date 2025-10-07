#!/usr/bin/env python3
"""
Heroku Deployment Script
Automates Heroku deployment and configuration
"""

import os
import subprocess
import json
import argparse
from datetime import datetime
import logging

class HerokuDeployer:
    def __init__(self):
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('heroku_deployment.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def run_command(self, command, check_output=False):
        """Run a shell command and return result"""
        try:
            self.logger.info(f"Running: {command}")
            if check_output:
                result = subprocess.check_output(command, shell=True, text=True)
                return result.strip()
            else:
                subprocess.run(command, shell=True, check=True)
                return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed: {command}")
            self.logger.error(f"Error: {e}")
            return False
    
    def check_heroku_cli(self):
        """Check if Heroku CLI is installed"""
        try:
            version = self.run_command('heroku --version', check_output=True)
            self.logger.info(f"Heroku CLI found: {version}")
            return True
        except:
            self.logger.error("Heroku CLI not found. Please install it first.")
            return False
    
    def check_heroku_login(self):
        """Check if user is logged into Heroku"""
        try:
            email = self.run_command('heroku auth:whoami', check_output=True)
            self.logger.info(f"Logged in as: {email}")
            return True
        except:
            self.logger.error("Not logged into Heroku. Run 'heroku login' first.")
            return False
    
    def create_heroku_files(self):
        """Create necessary Heroku configuration files"""
        # Create Procfile
        procfile_content = "web: gunicorn app:app\n"
        with open('Procfile', 'w') as f:
            f.write(procfile_content)
        self.logger.info("Created Procfile")
        
        # Create runtime.txt
        runtime_content = "python-3.11.5\n"
        with open('runtime.txt', 'w') as f:
            f.write(runtime_content)
        self.logger.info("Created runtime.txt")
        
        # Create app.json for Heroku Deploy Button
        app_json = {
            "name": "Portfolio Website",
            "description": "A modern portfolio website built with Flask",
            "keywords": ["python", "flask", "portfolio", "heroku"],
            "website": "https://github.com/yourusername/portfolio",
            "repository": "https://github.com/yourusername/portfolio",
            "logo": "https://your-portfolio.herokuapp.com/static/files/logo.png",
            "success_url": "/",
            "env": {
                "FLASK_SECRET_KEY": {
                    "description": "A secret key for Flask sessions",
                    "generator": "secret"
                },
                "GMAIL_USERNAME": {
                    "description": "Gmail username for sending emails"
                },
                "GMAIL_APP_PASSWORD": {
                    "description": "Gmail app password (not regular password)"
                },
                "ADMIN_EMAIL": {
                    "description": "Email address for admin notifications"
                }
            },
            "formation": {
                "web": {
                    "quantity": 1,
                    "size": "eco"
                }
            },
            "addons": [
                "heroku-redis:mini"
            ],
            "buildpacks": [
                {
                    "url": "heroku/python"
                }
            ]
        }
        
        with open('app.json', 'w') as f:
            json.dump(app_json, f, indent=2)
        self.logger.info("Created app.json")
    
    def create_heroku_app(self, app_name=None, region='us'):
        """Create a new Heroku app"""
        if not self.check_heroku_cli() or not self.check_heroku_login():
            return False
        
        try:
            if app_name:
                command = f'heroku create {app_name} --region {region}'
            else:
                command = f'heroku create --region {region}'
            
            result = self.run_command(command, check_output=True)
            
            # Extract app name from result
            if "https://" in result:
                app_url = result.split("https://")[1].split(" ")[0]
                app_name = app_url.split(".")[0]
                self.logger.info(f"✅ Created Heroku app: {app_name}")
                self.logger.info(f"🌐 URL: https://{app_url}")
                return app_name
            else:
                self.logger.error("Failed to parse app creation result")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to create Heroku app: {str(e)}")
            return False
    
    def set_environment_variables(self, app_name=None, env_vars=None):
        """Set environment variables on Heroku"""
        if env_vars is None:
            env_vars = self.get_required_env_vars()
        
        try:
            for key, value in env_vars.items():
                if value:  # Only set if value is provided
                    command = f'heroku config:set {key}="{value}"'
                    if app_name:
                        command += f' --app {app_name}'
                    
                    if not self.run_command(command):
                        return False
                else:
                    self.logger.warning(f"Skipping {key} - no value provided")
            
            self.logger.info("✅ Environment variables set successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to set environment variables: {str(e)}")
            return False
    
    def get_required_env_vars(self):
        """Get required environment variables"""
        return {
            'FLASK_SECRET_KEY': os.getenv('FLASK_SECRET_KEY', ''),
            'GMAIL_USERNAME': os.getenv('GMAIL_USERNAME', ''),
            'GMAIL_APP_PASSWORD': os.getenv('GMAIL_APP_PASSWORD', ''),
            'ADMIN_EMAIL': os.getenv('ADMIN_EMAIL', ''),
            'FLASK_ENV': 'production'
        }
    
    def deploy_to_heroku(self, app_name=None, branch='main'):
        """Deploy to Heroku"""
        try:
            # Check git status
            result = self.run_command('git status --porcelain', check_output=True)
            if result:
                self.logger.warning("Git working directory is not clean. Commit changes first.")
                return False
            
            # Deploy to Heroku
            command = f'git push heroku {branch}:main'
            if app_name:
                command = f'git push heroku-{app_name} {branch}:main'
            
            if not self.run_command(command):
                return False
            
            self.logger.info("✅ Deployment successful!")
            return True
            
        except Exception as e:
            self.logger.error(f"Deployment failed: {str(e)}")
            return False
    
    def setup_heroku_postgres(self, app_name=None, plan='mini'):
        """Setup Heroku Postgres (optional)"""
        try:
            command = f'heroku addons:create heroku-postgresql:{plan}'
            if app_name:
                command += f' --app {app_name}'
            
            if self.run_command(command):
                self.logger.info("✅ Heroku Postgres addon created")
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to setup Postgres: {str(e)}")
            return False
    
    def setup_heroku_redis(self, app_name=None, plan='mini'):
        """Setup Heroku Redis for caching"""
        try:
            command = f'heroku addons:create heroku-redis:{plan}'
            if app_name:
                command += f' --app {app_name}'
            
            if self.run_command(command):
                self.logger.info("✅ Heroku Redis addon created")
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to setup Redis: {str(e)}")
            return False
    
    def get_app_info(self, app_name=None):
        """Get Heroku app information"""
        try:
            command = 'heroku apps:info --json'
            if app_name:
                command += f' --app {app_name}'
            
            result = self.run_command(command, check_output=True)
            app_info = json.loads(result)
            
            return {
                'name': app_info['name'],
                'url': app_info['web_url'],
                'git_url': app_info['git_url'],
                'region': app_info['region']['name'],
                'created_at': app_info['created_at']
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get app info: {str(e)}")
            return None
    
    def full_deployment(self, app_name=None, staging=False):
        """Perform full deployment setup"""
        try:
            self.logger.info("🚀 Starting full Heroku deployment...")
            
            # Check prerequisites
            if not self.check_heroku_cli() or not self.check_heroku_login():
                return False
            
            # Create Heroku files
            self.create_heroku_files()
            
            # Create app if it doesn't exist
            if app_name:
                # Check if app exists
                try:
                    self.get_app_info(app_name)
                    self.logger.info(f"Using existing app: {app_name}")
                except:
                    app_name = self.create_heroku_app(app_name)
                    if not app_name:
                        return False
            else:
                app_name = self.create_heroku_app()
                if not app_name:
                    return False
            
            # Set environment variables
            if not self.set_environment_variables(app_name):
                return False
            
            # Setup addons (optional)
            self.setup_heroku_redis(app_name)
            
            # Deploy
            if not self.deploy_to_heroku(app_name):
                return False
            
            # Get final app info
            app_info = self.get_app_info(app_name)
            if app_info:
                self.logger.info("🎉 Deployment completed successfully!")
                self.logger.info(f"📱 App Name: {app_info['name']}")
                self.logger.info(f"🌐 URL: {app_info['url']}")
                self.logger.info(f"📍 Region: {app_info['region']}")
                
                # Save deployment info
                deployment_info = {
                    'deployed_at': datetime.now().isoformat(),
                    'app_info': app_info,
                    'environment': 'staging' if staging else 'production'
                }
                
                with open('deployment_info.json', 'w') as f:
                    json.dump(deployment_info, f, indent=2)
                
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Full deployment failed: {str(e)}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Portfolio Heroku Deployment Script')
    parser.add_argument('action', choices=['deploy', 'create', 'setup', 'info', 'logs'], 
                       help='Action to perform')
    parser.add_argument('--app-name', '-a', help='Heroku app name')
    parser.add_argument('--staging', action='store_true', help='Deploy to staging')
    parser.add_argument('--branch', '-b', default='main', help='Git branch to deploy')
    
    args = parser.parse_args()
    
    deployer = HerokuDeployer()
    
    try:
        if args.action == 'deploy':
            success = deployer.full_deployment(args.app_name, args.staging)
            if success:
                print("✅ Full deployment successful!")
                return 0
            else:
                print("❌ Deployment failed!")
                return 1
                
        elif args.action == 'create':
            app_name = deployer.create_heroku_app(args.app_name)
            if app_name:
                print(f"✅ Created app: {app_name}")
                return 0
            else:
                print("❌ App creation failed!")
                return 1
                
        elif args.action == 'setup':
            deployer.create_heroku_files()
            print("✅ Heroku files created!")
            return 0
            
        elif args.action == 'info':
            app_info = deployer.get_app_info(args.app_name)
            if app_info:
                print("📊 App Information:")
                for key, value in app_info.items():
                    print(f"   {key}: {value}")
                return 0
            else:
                print("❌ Failed to get app info!")
                return 1
                
        elif args.action == 'logs':
            command = 'heroku logs --tail'
            if args.app_name:
                command += f' --app {args.app_name}'
            
            print("📋 Viewing Heroku logs (Ctrl+C to exit):")
            deployer.run_command(command)
            return 0
    
    except KeyboardInterrupt:
        print("\n👋 Deployment interrupted by user")
        return 0
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1

if __name__ == '__main__':
    exit(main())