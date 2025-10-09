# 🚀 Heroku Deployment Guide for Portfolio Website

## Prerequisites Complete ✅
Your project is already configured for Heroku deployment with:
- ✅ `Procfile` (gunicorn configuration)
- ✅ `requirements.txt` (all dependencies)
- ✅ `runtime.txt` (Python 3.12.6)
- ✅ `app.json` (Heroku app configuration)
- ✅ Environment variables setup

## Step 1: Install Heroku CLI

### Option A: Download Installer (Recommended)
1. Go to: https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli
2. Download "Windows x64 Installer"
3. Run the installer
4. Restart your terminal/PowerShell

### Option B: PowerShell Installation
```powershell
# Install using npm (if you have Node.js)
npm install -g heroku

# OR install using winget (alternative source)
winget install --id Heroku.HerokuCLI
```

## Step 2: Login to Heroku
```bash
heroku login
# This will open a browser for authentication
```

## Step 3: Create Heroku App
```bash
# Create app with a specific name (replace 'your-portfolio-name')
heroku create mahanth-portfolio

# OR let Heroku generate a random name
heroku create
```

## Step 4: Set Environment Variables
```bash
# Set all required environment variables
heroku config:set FLASK_SECRET_KEY="your-super-secret-key-here"
heroku config:set FLASK_ENV="production"
heroku config:set GMAIL_USERNAME="perlamahanth@gmail.com"
heroku config:set GMAIL_APP_PASSWORD="kcldqadeauugkwdv"
heroku config:set ADMIN_EMAIL="perlamahanth@gmail.com"

# Verify variables are set
heroku config
```

## Step 5: Deploy to Heroku
```bash
# Make sure all changes are committed
git add .
git commit -m "Prepare for Heroku deployment"

# Deploy to Heroku
git push heroku main

# If you're on a different branch:
git push heroku your-branch-name:main
```

## Step 6: Open Your Live Website
```bash
heroku open
```

## Alternative: One-Click Deploy Button

You can also deploy directly from GitHub using Heroku's deploy button:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Useful Heroku Commands

```bash
# View app logs
heroku logs --tail

# View app info
heroku apps:info

# Scale dynos
heroku ps:scale web=1

# Run database migrations (if needed)
heroku run python manage.py migrate

# Restart app
heroku restart

# Open Heroku dashboard
heroku dashboard
```

## Troubleshooting

### Common Issues:

1. **Build Failed**: Check that all dependencies are in `requirements.txt`
2. **App Crashed**: Check logs with `heroku logs --tail`
3. **Environment Variables**: Verify with `heroku config`
4. **Static Files**: Make sure Flask serves static files correctly

### Environment Variables Needed:
- `FLASK_SECRET_KEY`: Random secret key for sessions
- `FLASK_ENV`: Set to "production"
- `GMAIL_USERNAME`: Your Gmail address
- `GMAIL_APP_PASSWORD`: Your Gmail App Password (16 characters)
- `ADMIN_EMAIL`: Email for admin notifications

## Post-Deployment Checklist

- [ ] Website loads correctly
- [ ] Contact form works
- [ ] Admin panel accessible
- [ ] Email sending functional
- [ ] All static files loading
- [ ] SSL certificate active (automatically provided by Heroku)

## Custom Domain (Optional)

If you want to use a custom domain:

```bash
# Add custom domain
heroku domains:add www.your-domain.com

# Get DNS target
heroku domains

# Configure your DNS provider to point to the Heroku DNS target
```

## Security Notes

- Environment variables are secure on Heroku
- SSL is automatically provided
- App runs in isolated dynos
- Regular security updates from Heroku

Your portfolio is ready for professional deployment! 🎉