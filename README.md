# 🌟 Professional Portfolio Website - Mahanth Perla# Portfolio Website - Computer Engineer



[![Portfolio Status](https://img.shields.io/badge/Status-Live-brightgreen)](https://github.com/mahaperla/portfolio)A modern, responsive portfolio website built with Flask for computer engineers and tech professionals.

[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)

[![Flask](https://img.shields.io/badge/Flask-3.0.0-red)](https://flask.palletsprojects.com)## 🚀 Features

[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple)](https://getbootstrap.com)

[![SEO](https://img.shields.io/badge/SEO-Optimized-green)](https://github.com/mahaperla/portfolio)- **🎨 Modern Design**: Responsive layout with dark mode toggle and tech-themed animations

- **🔒 Advanced Security**: Temporary password system with 30-minute auto-expiration and email delivery

> A modern, responsive, and SEO-optimized portfolio website for Network Engineer Mahanth Perla, built with Flask and featuring a comprehensive admin panel for content management.- **📧 Contact Integration**: Gmail SMTP integration with contact form validation

- **🎯 Dynamic Content**: JSON-based content management system

## 🚀 **Live Demo**- **⚡ Performance**: Flask-Caching for optimized loading

- **📱 Mobile-Ready**: Bootstrap 5 responsive design

🔗 **[View Live Portfolio](https://your-domain.com)** *(Replace with your deployed URL)*- **🔧 Admin Panel**: Password-protected content management interface

- **📊 Comprehensive Logging**: Security, access, and error logging

## 📋 **Table of Contents**- **🚀 Easy Deployment**: Automated scripts for GitHub and Heroku deployment



- [Features](#-features)## 🛠️ Technology Stack

- [Tech Stack](#-tech-stack)

- [Installation](#-installation)- **Backend**: Python Flask

- [Usage](#-usage)- **Frontend**: Bootstrap 5, JavaScript (ES6+), Particles.js

- [Project Structure](#-project-structure)- **Email**: Flask-Mail with Gmail SMTP

- [SEO Features](#-seo-features)- **Security**: Bcrypt, temporary password system

- [Admin Panel](#-admin-panel)- **Deployment**: Heroku with automatic HTTPS

- [API Documentation](#-api-documentation)- **Caching**: Flask-Caching

- [Deployment](#-deployment)

- [Contributing](#-contributing)## 📋 Prerequisites

- [License](#-license)

- [Contact](#-contact)- Python 3.11+

- Gmail account with app password enabled

## ✨ **Features**- Git (for deployment)

- Heroku CLI (for Heroku deployment)

### 🎨 **Frontend Features**

- **Single-Page Application**: Smooth scrolling between sections## 🚀 Quick Start

- **Responsive Design**: Mobile-first, works on all devices

- **Dark/Light Theme**: User preference toggle### 1. Setup Virtual Environment

- **Animated Background**: Particles.js integration

- **Typing Animation**: Dynamic name typing effect```bash

- **Expandable Content**: Click to reveal more details# Navigate to your app directory

- **Resume Downloads**: PDF and Word format optionscd app

- **Contact Form**: AJAX-powered with modal success messages

# Activate the virtual environment (you already have this)

### 🔧 **Backend Features**.\Scripts\activate  # Windows

- **Flask Framework**: Modern Python web development# source venv/bin/activate  # macOS/Linux

- **Admin Panel**: Complete content management system

- **Modal Editing**: User-friendly content updates# Install dependencies

- **File Management**: Resume upload and download systempip install -r requirements.txt

- **Email Integration**: Contact form with Gmail SMTP```

- **Session Management**: Secure admin authentication

- **Logging System**: Comprehensive request/error logging### 2. Configure Environment Variables

- **Backup & Restore**: Complete data backup functionality

Create a `.env` file in the app directory:

### 🔍 **SEO Optimization**

- **Meta Tags**: Complete Open Graph and Twitter Cards```bash

- **Structured Data**: JSON-LD for rich search results# Copy the example file

- **XML Sitemap**: Dynamic sitemap generationcopy .env.example .env

- **Robots.txt**: Search engine crawling optimization

- **Canonical URLs**: 301 redirects and clean URLs# Edit .env with your actual values:

- **Performance**: Optimized loading and cachingFLASK_SECRET_KEY=your-super-secret-key-here-generate-a-random-string

- **Accessibility**: Screen reader and keyboard friendlyFLASK_ENV=development  # Change to 'production' for production

GMAIL_USERNAME=your_email@gmail.com

## 🛠 **Tech Stack**GMAIL_APP_PASSWORD=your_16_character_gmail_app_password

ADMIN_EMAIL=your_email@gmail.com

### **Backend**```

- **Python 3.8+**: Core programming language

- **Flask 3.0.0**: Web framework### 3. Gmail App Password Setup

- **Flask-Mail**: Email functionality

- **Flask-Caching**: Performance optimization1. Go to [Google Account Settings](https://myaccount.google.com/)

- **Werkzeug**: Security utilities2. Security → 2-Step Verification (enable if not already)

- **Python-dotenv**: Environment management3. App passwords → Generate app password for "Mail"

4. Use the 16-character password in your `.env` file

### **Frontend**

- **HTML5**: Semantic markup### 4. Update Content

- **CSS3**: Modern styling with CSS Grid/Flexbox

- **JavaScript (ES6+)**: Interactive functionalityEdit the JSON files in the `data/` directory:

- **Bootstrap 5.3.0**: UI framework- `home.json` - Home page content and personal info

- **Font Awesome 6**: Icon library- `about.json` - Education, certifications, and skills

- **Particles.js**: Animated backgrounds- `experience.json` - Work experience and projects

- **Google Fonts**: Typography (Poppins, Fira Code)

### 5. Add Your Resume

### **Tools & Services**

- **Git**: Version controlPlace your resume PDF file as `static/files/resume.pdf`

- **Gmail SMTP**: Email delivery

- **JSON**: Data storage### 6. Run the Application

- **Backup System**: Data protection

```bash

## 🚀 **Installation**python app.py

```

### **Prerequisites**

- Python 3.8 or higherVisit `http://localhost:5000` to see your portfolio!

- Git

- Gmail account (for contact form)## 🔐 Admin Panel



### **Quick Start**1. Access `/admin/login`

2. Check your email for the temporary password (sent automatically on startup)

1. **Clone the repository**3. Passwords regenerate every 30 minutes for security

   ```bash

   git clone https://github.com/mahaperla/portfolio.git## 📁 Project Structure

   cd portfolio

   ``````

app/

2. **Create virtual environment**├── static/                 # Static files (CSS, JS, images)

   ```bash│   ├── css/

   python -m venv app│   ├── js/

   cd app│   └── files/             # Resume and other files

   # On Windows:├── templates/             # HTML templates

   Scripts\\activate│   ├── admin/            # Admin panel templates

   # On macOS/Linux:│   └── errors/           # Error pages

   source bin/activate├── data/                 # JSON content files

   ```├── utils/                # Utility modules

├── logs/                 # Application logs

3. **Install dependencies**├── app.py               # Main Flask application

   ```bash├── settings.json        # Application settings

   pip install flask flask-mail flask-caching python-dotenv werkzeug├── requirements.txt     # Python dependencies

   ```└── deployment files    # Heroku and deployment configs

```

4. **Set up environment variables**

   ```bash## 🚀 Deployment

   # Create .env file in the app directory

   MAIL_USERNAME=your-email@gmail.com### GitHub Deployment

   MAIL_PASSWORD=your-app-password

   ADMIN_EMAIL=your-admin-email@gmail.com```bash

   SECRET_KEY=your-secret-key-here# Setup repository (if not already done)

   ```python github_deploy.py setup --repo-url https://github.com/yourusername/portfolio.git



5. **Run the application**# Deploy to GitHub

   ```bashpython github_deploy.py deploy --message "Initial portfolio deployment"

   python app.py```

   ```

### Heroku Deployment

6. **Access the website**

   - Portfolio: `http://localhost:5000````bash

   - Admin Panel: `http://localhost:5000/admin`# Full deployment (creates app, sets environment, deploys)

python heroku_deploy.py deploy --app-name your-portfolio-name

## 💻 **Usage**

# Or deploy to existing app

### **Public Portfolio**python heroku_deploy.py deploy

- Visit the homepage to view the complete portfolio```

- Use navigation to jump between sections

- Download resume in PDF or Word format### Manual Heroku Setup

- Contact via the integrated form

```bash

### **Admin Panel**# Install Heroku CLI and login

- Access `/admin` for content managementheroku login

- Edit personal information, education, experience

- Upload new resume files# Create app

- View contact form submissionsheroku create your-portfolio-name

- Backup and restore data

# Set environment variables

### **Content Management**heroku config:set FLASK_SECRET_KEY="your-secret-key"

- All content is stored in JSON files in the `data/` directoryheroku config:set GMAIL_USERNAME="your-email@gmail.com"

- Edit directly or use the admin panelheroku config:set GMAIL_APP_PASSWORD="your-app-password"

- Changes reflect immediately on the websiteheroku config:set ADMIN_EMAIL="your-email@gmail.com"



## 📁 **Project Structure**# Deploy

git push heroku main

``````

portfolio/

├── app/## 🛠️ Utility Scripts

│   ├── data/                      # JSON data files

│   │   ├── home.json             # Personal info and hero section### Backup & Restore

│   │   ├── about.json            # Education, skills, certifications

│   │   └── experience.json       # Work experience```bash

│   ├── static/                   # Static assets# Create backup

│   │   ├── css/python backup_restore.py backup

│   │   │   └── style.css        # Main stylesheet

│   │   ├── js/# List backups

│   │   │   ├── home.js          # Homepage interactionspython backup_restore.py list

│   │   │   ├── main.js          # Global JavaScript

│   │   │   └── particles-config.js # Particles.js config# Restore from backup

│   │   ├── files/               # Uploaded files (resumes)python backup_restore.py restore --file backups/portfolio_backup_20241005_120000.zip

│   │   ├── images/              # Image assets```

│   │   └── robots.txt           # SEO crawling instructions

│   ├── templates/               # Jinja2 templates### GitHub Operations

│   │   ├── admin/               # Admin panel templates

│   │   ├── base.html            # Base template```bash

│   │   ├── single_page.html     # Main portfolio page# Check repository status

│   │   └── sitemap.xml          # Dynamic sitemappython github_deploy.py status

│   ├── backups/                 # Automatic backups

│   ├── logs/                    # Application logs# Deploy with custom message

│   ├── app.py                   # Main Flask applicationpython github_deploy.py deploy --message "Updated portfolio content"

│   ├── backup_restore.py        # Backup/restore utilities```

│   ├── optimize_images.py       # Image optimization

│   ├── .env                     # Environment variables### Heroku Operations

│   └── requirements.txt         # Python dependencies

├── README.md                    # This file```bash

└── .gitignore                   # Git ignore rules# Check app info

```python heroku_deploy.py info --app-name your-app



## 🔍 **SEO Features**# View logs

python heroku_deploy.py logs --app-name your-app

This portfolio is fully optimized for search engines:```



- **Meta Tags**: Dynamic titles, descriptions, keywords## 🔧 Customization

- **Open Graph**: Social media sharing optimization

- **Twitter Cards**: Enhanced Twitter previews### Themes and Colors

- **Structured Data**: JSON-LD for rich snippets- Edit `static/css/style.css` for styling changes

- **XML Sitemap**: `/sitemap.xml` for search engines- Modify CSS variables at the top of the file for color schemes

- **Robots.txt**: `/robots.txt` for crawler instructions

- **Canonical URLs**: Clean, consistent URL structure### Animations

- **Performance**: Fast loading with caching headers- Particles.js configuration in `static/js/particles-config.js`

- Custom animations in `static/js/main.js`

## 🔐 **Admin Panel**

### Email Templates

The admin panel provides comprehensive content management:- Modify email templates in `utils/security.py` and `app.py`



### **Features**## 🔒 Security Features

- **Content Editing**: Modal-based editing for all sections

- **File Management**: Upload/download resumes- **Temporary Passwords**: Auto-generated every 30 minutes

- **Data Backup**: Complete backup and restore system- **Secure Hashing**: Bcrypt for password storage

- **Security**: Session-based authentication- **Input Validation**: Server and client-side validation

- **Logging**: View all admin actions and errors- **CSRF Protection**: Built-in Flask security

- **Comprehensive Logging**: Security event tracking

### **Access**- **Environment Variables**: Sensitive data protection

1. Navigate to `/admin`

2. Admin panel is secured with session management## 📊 Monitoring

3. Use the integrated editing modals to update content

### Logs Location

## 📡 **API Documentation**- `logs/portfolio.log` - General application logs

- `logs/errors.log` - Error logs only

### **Public Endpoints**- `logs/security.log` - Security events

- `GET /` - Main portfolio page- `logs/access.log` - HTTP access logs

- `GET /sitemap.xml` - XML sitemap

- `GET /robots.txt` - Robots.txt file### Performance

- `GET /download/resume/<format>` - Resume download (pdf/word)- Flask-Caching enabled for JSON data

- `POST /contact-ajax` - Contact form submission- Optimized static file serving

- Lazy loading for images

### **Admin Endpoints**

- `GET /admin` - Admin dashboard## 🚨 Troubleshooting

- `POST /admin/upload-resume` - Resume file upload

- `POST /admin/backup` - Create data backup### Common Issues

- `POST /admin/restore` - Restore from backup

1. **Email not working**: Check Gmail app password and 2FA settings

## 🚀 **Deployment**2. **Admin password not received**: Check spam folder and email settings

3. **Heroku deployment fails**: Ensure all environment variables are set

### **Environment Setup**4. **Static files not loading**: Check file paths and Heroku static file serving

1. Set production environment variables

2. Configure SMTP settings for contact form### Debug Mode

3. Update domain in canonical URLs and sitemap

Set `FLASK_ENV=development` in `.env` for detailed error messages.

### **Popular Deployment Options**

- **Heroku**: Easy Python app deployment## 📄 License

- **DigitalOcean**: VPS with full control

- **AWS**: Scalable cloud deploymentThis project is licensed under the MIT License.

- **PythonAnywhere**: Simple Python hosting

## 🤝 Contributing

### **Production Considerations**

- Use a production WSGI server (Gunicorn)1. Fork the repository

- Enable HTTPS for security2. Create a feature branch

- Set up domain and DNS3. Make your changes

- Configure error monitoring4. Test thoroughly

5. Submit a pull request

## 🤝 **Contributing**

## 📞 Support

Contributions are welcome! Please feel free to submit a Pull Request.

For issues or questions:

1. Fork the repository- Check the logs in the `logs/` directory

2. Create your feature branch (`git checkout -b feature/AmazingFeature`)- Review the troubleshooting section

3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)- Contact: your.email@gmail.com

4. Push to the branch (`git push origin feature/AmazingFeature`)

5. Open a Pull Request---



## 📄 **License****Built with ❤️ for Computer Engineers**



This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.Last updated: October 2024

## 📞 **Contact**

**Mahanth Perla** - Network Engineer

- 🌐 **Portfolio**: [Live Demo](https://your-domain.com)
- 💼 **LinkedIn**: [linkedin.com/in/mahanthperla](https://www.linkedin.com/in/mahanthperla/)
- 📧 **Email**: [perlamahanth@gmail.com](mailto:perlamahanth@gmail.com)
- 📱 **Phone**: +1 (720) 761-7479
- 🏠 **Location**: Irvine, California
- 💻 **GitHub**: [github.com/mahaperla](https://github.com/mahaperla)

---

## 🌟 **Features Showcase**

### **Single-Page Design**
- Smooth scrolling navigation
- Responsive mobile-first design
- Professional animations and effects

### **Admin Content Management**
- Real-time content editing
- File upload and management
- Complete backup system

### **SEO Optimization**
- Google-ready structured data
- Social media optimization
- Search engine friendly URLs

### **Performance**
- Fast loading times
- Optimized images and assets
- Caching and compression

---

**⭐ If you find this portfolio helpful, please give it a star on GitHub!**

*Built with ❤️ by Mahanth Perla using Flask, Bootstrap, and modern web technologies.*