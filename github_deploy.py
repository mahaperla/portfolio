#!/usr/bin/env python3
"""
GitHub Deployment Script
Automates Git operations for portfolio deployment
"""

import os
import subprocess
import json
import argparse
from datetime import datetime
import logging

class GitHubDeployer:
    def __init__(self):
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        self.setup_logging()
        self.check_git_repo()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('deployment.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def check_git_repo(self):
        """Check if we're in a git repository"""
        if not os.path.exists('.git'):
            self.logger.warning("Not in a git repository. Initialize with 'git init' first.")
    
    def run_command(self, command, check_output=False):
        """Run a shell command and return result"""
        try:
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
    
    def check_git_status(self):
        """Check git status and return information"""
        try:
            status = self.run_command('git status --porcelain', check_output=True)
            modified_files = []
            untracked_files = []
            
            if status:
                for line in status.split('\n'):
                    if line.strip():
                        status_code = line[:2]
                        file_path = line[3:]
                        
                        if status_code == '??':
                            untracked_files.append(file_path)
                        else:
                            modified_files.append(file_path)
            
            return {
                'clean': len(modified_files) == 0 and len(untracked_files) == 0,
                'modified': modified_files,
                'untracked': untracked_files
            }
        except:
            return {'clean': False, 'modified': [], 'untracked': []}
    
    def get_current_branch(self):
        """Get current git branch"""
        return self.run_command('git branch --show-current', check_output=True)
    
    def get_remote_info(self):
        """Get remote repository information"""
        try:
            remote_url = self.run_command('git remote get-url origin', check_output=True)
            return remote_url
        except:
            return None
    
    def create_gitignore(self):
        """Create or update .gitignore file"""
        gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Environment variables
.env
.venv
env/
venv/
ENV/

# Flask
instance/

# Logs
logs/*.log
*.log

# Backup files
backups/
*.backup

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp

# Temporary files
temp/
tmp/
*.tmp

# Local settings
local_settings.py
"""
        
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        
        self.logger.info("Created/updated .gitignore file")
    
    def prepare_deployment(self, commit_message=None):
        """Prepare files for deployment"""
        self.logger.info("Preparing deployment...")
        
        # Create .gitignore if it doesn't exist
        if not os.path.exists('.gitignore'):
            self.create_gitignore()
        
        # Check if .env.example exists, if not create it
        if not os.path.exists('.env.example'):
            self.create_env_example()
        
        # Remove any sensitive files that shouldn't be committed
        sensitive_files = ['.env', 'temp_admin_password.txt']
        for file in sensitive_files:
            if os.path.exists(file):
                os.remove(file)
                self.logger.info(f"Removed sensitive file: {file}")
        
        # Update README.md
        self.update_readme()
    
    def create_env_example(self):
        """Create .env.example file"""
        env_example = """# Flask Portfolio Environment Variables
# Copy this to .env and fill in your actual values

# Flask Configuration
FLASK_SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production

# Email Configuration (Gmail App Password)
GMAIL_USERNAME=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_character_app_password

# Admin Configuration
ADMIN_EMAIL=your_email@gmail.com

# Heroku Configuration (set these in Heroku dashboard)
# PORT will be set automatically by Heroku
"""
        
        with open('.env.example', 'w') as f:
            f.write(env_example)
        
        self.logger.info("Created .env.example file")
    
    def update_readme(self):
        """Create or update README.md"""
        readme_content = f"""# Portfolio Website

A modern, responsive portfolio website built with Flask for computer engineers and tech professionals.

## Features

- 🎨 Modern responsive design with dark mode toggle
- 🔒 Secure admin panel with temporary password system
- 📧 Contact form with email integration
- 🎯 Dynamic content management via JSON files
- 🚀 Animated backgrounds and smooth transitions
- 📱 Mobile-friendly responsive layout
- 🔧 Easy deployment to Heroku

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: Bootstrap 5, JavaScript (ES6+)
- **Email**: Flask-Mail with Gmail SMTP
- **Deployment**: Heroku
- **Security**: Bcrypt password hashing, CSRF protection

## Quick Start

1. Clone the repository:
```bash
git clone <your-repo-url>
cd portfolio
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup environment variables:
```bash
cp .env.example .env
# Edit .env with your actual values
```

5. Run the application:
```bash
python app.py
```

## Deployment

### Heroku Deployment

1. Install Heroku CLI
2. Run the deployment script:
```bash
python heroku_deploy.py deploy
```

### Manual Heroku Deployment

1. Create Heroku app:
```bash
heroku create your-portfolio-name
```

2. Set environment variables:
```bash
heroku config:set FLASK_SECRET_KEY="your-secret-key"
heroku config:set GMAIL_USERNAME="your-email@gmail.com"
heroku config:set GMAIL_APP_PASSWORD="your-app-password"
heroku config:set ADMIN_EMAIL="your-email@gmail.com"
```

3. Deploy:
```bash
git push heroku main
```

## Admin Panel

Access the admin panel at `/admin/login`. The system automatically generates temporary passwords every 30 minutes and emails them to your configured admin email.

## Content Management

Content is managed through JSON files in the `data/` directory:
- `home.json` - Home page content
- `about.json` - About page content  
- `experience.json` - Experience and projects

## Scripts

- `backup_restore.py` - Backup and restore portfolio data
- `github_deploy.py` - GitHub deployment automation
- `heroku_deploy.py` - Heroku deployment automation

## Security Features

- Temporary password system with automatic expiration
- Secure password hashing with bcrypt
- CSRF protection on forms
- Input validation and sanitization
- Comprehensive logging

## License

This project is licensed under the MIT License.

## Last Updated

{datetime.now().strftime('%Y-%m-%d')}
"""
        
        with open('README.md', 'w') as f:
            f.write(readme_content)
        
        self.logger.info("Updated README.md")
    
    def deploy_to_github(self, commit_message=None, branch='main', force=False):
        """Deploy to GitHub"""
        if commit_message is None:
            commit_message = f"Portfolio update - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        try:
            # Prepare deployment
            self.prepare_deployment(commit_message)
            
            # Check git status
            status = self.check_git_status()
            
            if status['clean'] and not force:
                self.logger.info("Repository is clean, nothing to deploy")
                return True
            
            # Show status
            if status['modified']:
                self.logger.info(f"Modified files: {', '.join(status['modified'])}")
            if status['untracked']:
                self.logger.info(f"Untracked files: {', '.join(status['untracked'])}")
            
            # Add all files
            self.logger.info("Adding files to git...")
            if not self.run_command('git add .'):
                return False
            
            # Commit changes
            self.logger.info(f"Committing changes: {commit_message}")
            if not self.run_command(f'git commit -m "{commit_message}"'):
                return False
            
            # Push to remote
            current_branch = self.get_current_branch()
            if current_branch != branch:
                self.logger.info(f"Switching to branch: {branch}")
                self.run_command(f'git checkout -b {branch}')
            
            self.logger.info(f"Pushing to origin/{branch}...")
            if not self.run_command(f'git push origin {branch}'):
                return False
            
            # Show remote info
            remote_url = self.get_remote_info()
            if remote_url:
                self.logger.info(f"✅ Successfully deployed to: {remote_url}")
            else:
                self.logger.info("✅ Successfully deployed to GitHub")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Deployment failed: {str(e)}")
            return False
    
    def setup_github_repo(self, repo_url=None):
        """Setup GitHub repository"""
        try:
            if not os.path.exists('.git'):
                self.logger.info("Initializing git repository...")
                self.run_command('git init')
            
            if repo_url:
                self.logger.info(f"Adding remote origin: {repo_url}")
                self.run_command(f'git remote add origin {repo_url}')
            
            self.create_gitignore()
            self.prepare_deployment()
            
            self.logger.info("✅ GitHub repository setup complete")
            return True
            
        except Exception as e:
            self.logger.error(f"Repository setup failed: {str(e)}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Portfolio GitHub Deployment Script')
    parser.add_argument('action', choices=['deploy', 'setup', 'status'], 
                       help='Action to perform')
    parser.add_argument('--message', '-m', help='Commit message')
    parser.add_argument('--branch', '-b', default='main', help='Branch to deploy to')
    parser.add_argument('--repo-url', help='GitHub repository URL (for setup)')
    parser.add_argument('--force', action='store_true', help='Force deploy even if no changes')
    
    args = parser.parse_args()
    
    deployer = GitHubDeployer()
    
    try:
        if args.action == 'deploy':
            success = deployer.deploy_to_github(
                commit_message=args.message,
                branch=args.branch,
                force=args.force
            )
            if success:
                print("✅ Deployment successful!")
                return 0
            else:
                print("❌ Deployment failed!")
                return 1
                
        elif args.action == 'setup':
            success = deployer.setup_github_repo(args.repo_url)
            if success:
                print("✅ Repository setup successful!")
                return 0
            else:
                print("❌ Repository setup failed!")
                return 1
                
        elif args.action == 'status':
            status = deployer.check_git_status()
            current_branch = deployer.get_current_branch()
            remote_url = deployer.get_remote_info()
            
            print(f"📊 Git Status:")
            print(f"   Current branch: {current_branch}")
            print(f"   Remote: {remote_url or 'Not set'}")
            print(f"   Status: {'Clean' if status['clean'] else 'Has changes'}")
            
            if status['modified']:
                print(f"   Modified files: {len(status['modified'])}")
                for file in status['modified'][:5]:  # Show first 5
                    print(f"     - {file}")
                if len(status['modified']) > 5:
                    print(f"     ... and {len(status['modified']) - 5} more")
            
            if status['untracked']:
                print(f"   Untracked files: {len(status['untracked'])}")
                for file in status['untracked'][:5]:  # Show first 5
                    print(f"     - {file}")
                if len(status['untracked']) > 5:
                    print(f"     ... and {len(status['untracked']) - 5} more")
            
            return 0
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1

if __name__ == '__main__':
    exit(main())