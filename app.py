from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_file
from flask_mail import Mail, Message
from flask_caching import Cache
import json
import os
import logging
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.utils import secure_filename
import traceback
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Import custom utilities
from utils.security import get_security_manager, init_security_system
from utils.logger import setup_logging, log_request, log_security_event, log_admin_action

# Initialize Flask app
app = Flask(__name__)

# Load configuration
def load_settings():
    """Load settings from JSON file"""
    settings_path = os.path.join(os.path.dirname(__file__), 'settings.json')
    try:
        with open(settings_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"settings.json not found at {settings_path}")
        return {
            'email': {
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'use_tls': True
            },
            'contact_form': {
                'success_message': 'Thank you for your message!',
                'error_message': 'Error sending message.'
            },
            'security': {
                'password_reset_interval_minutes': 30,
                'session_timeout_hours': 2
            }
        }

settings = load_settings()

# Flask configuration
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-key-change-in-production')
app.config['DEBUG'] = os.getenv('FLASK_ENV') != 'production'

# Mail configuration
app.config['MAIL_SERVER'] = settings['email']['smtp_server']
app.config['MAIL_PORT'] = settings['email']['smtp_port']
app.config['MAIL_USE_TLS'] = settings['email']['use_tls']
app.config['MAIL_USE_SSL'] = False  # TLS and SSL are mutually exclusive
app.config['MAIL_USERNAME'] = os.getenv('GMAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('GMAIL_APP_PASSWORD')

# Cache configuration
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

# Initialize extensions
mail = Mail(app)
cache = Cache(app)

# Setup logging
logger = setup_logging(app)

# Initialize security system
security_manager = get_security_manager()

@app.context_processor
def inject_current_year():
    """Inject current year into all templates"""
    return dict(current_year=datetime.now().year)

def load_json_data(filename):
    """Load data from JSON file with caching"""
    @cache.memoize(timeout=300)
    def _load_data(file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Data file {file_path} not found")
            return {}
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in {file_path}")
            return {}
    
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', filename)
    return _load_data(file_path)

def save_json_data(filename, data):
    """Save data to JSON file and clear cache"""
    try:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', filename)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        
        # Clear all cache to ensure fresh data
        cache.clear()
        logger.info(f"Successfully saved {filename} and cleared cache")
        return True
    except Exception as e:
        logger.error(f"Error saving {filename}: {str(e)}")
        return False

def admin_required(f):
    """Decorator to require admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_authenticated' not in session:
            log_security_event("Unauthorized admin access attempt", "No session", request)
            # Check if this is an AJAX request
            if request.is_json or 'application/json' in request.headers.get('Content-Type', ''):
                return jsonify({'success': False, 'message': 'Authentication required', 'redirect': '/admin/login'}), 401
            return redirect(url_for('admin_login'))
        
        # Check if session is still valid
        if 'admin_login_time' in session:
            login_time = datetime.fromisoformat(session['admin_login_time'])
            if datetime.now() - login_time > timedelta(hours=settings['security']['session_timeout_hours']):
                session.clear()
                log_security_event("Admin session expired", "Session timeout", request)
                if request.is_json or 'application/json' in request.headers.get('Content-Type', ''):
                    return jsonify({'success': False, 'message': 'Session expired', 'redirect': '/admin/login'}), 401
                flash('Session expired. Please login again.', 'warning')
                return redirect(url_for('admin_login'))
        
        return f(*args, **kwargs)
    
    return decorated_function

@app.before_request
def before_request():
    """Handle URL canonicalization and redirects"""
    # Log all requests
    log_request(request)
    
    # Force HTTPS in production (if not localhost)
    if not app.debug and not request.is_secure and request.headers.get('Host', '').split(':')[0] not in ['localhost', '127.0.0.1']:
        return redirect(request.url.replace('http://', 'https://'), code=301)
    
    # Remove trailing slashes for SEO (except root)
    if len(request.path) > 1 and request.path.endswith('/'):
        return redirect(request.path.rstrip('/'), code=301)
    
    # Redirect common variations to canonical URLs
    canonical_redirects = {
        '/index': '/',
        '/index.html': '/',
        '/home': '/',
        '/portfolio.html': '/',
        '/about.html': '/#about',
        '/contact.html': '/#contact',
        '/experience.html': '/#experience'
    }
    
    if request.path in canonical_redirects:
        return redirect(canonical_redirects[request.path], code=301)

@app.after_request
def after_request(response):
    """Add SEO and security headers"""
    log_request(request, response.status_code)
    
    # SEO and Security Headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Cache control for static assets
    if request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=31536000'  # 1 year
    elif request.path in ['/', '/portfolio']:
        response.headers['Cache-Control'] = 'public, max-age=3600'  # 1 hour
    
    return response

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return render_template('errors/500.html'), 500

# Main routes
@app.route('/')
def home():
    """Single page portfolio with all sections"""
    home_data = load_json_data('home.json')
    about_data = load_json_data('about.json')
    experience_data = load_json_data('experience.json')
    
    return render_template('single_page.html', 
                         home_data=home_data,
                         about_data=about_data,
                         experience_data=experience_data)

@app.route('/home')
def home_separate():
    """Separate Home page (for admin editing)"""
    data = load_json_data('home.json')
    return render_template('home.html', data=data)

@app.route('/about')
def about():
    """About page"""
    data = load_json_data('about.json')
    return render_template('about.html', data=data)

@app.route('/experience')
def experience():
    """Experience page"""
    data = load_json_data('experience.json')
    return render_template('experience.html', data=data)

@app.route('/resume')
def resume():
    """Resume page with download option"""
    resume_path = 'static/files/resume.pdf'
    if os.path.exists(resume_path):
        return render_template('resume.html', resume_available=True)
    else:
        return render_template('resume.html', resume_available=False)

@app.route('/download-resume/<format>')
def download_resume(format):
    """Download resume in specified format (pdf or word)"""
    if format == 'pdf':
        resume_path = 'static/files/resume.pdf'
        filename = 'Mahanth_Perla_Resume.pdf'
        mimetype = 'application/pdf'
    elif format == 'word':
        resume_path = 'static/files/resume.docx'
        filename = 'Mahanth_Perla_Resume.docx'
        mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    else:
        flash('Invalid resume format requested.', 'error')
        return redirect(url_for('home'))
    
    if os.path.exists(resume_path):
        log_admin_action(f"Resume downloaded ({format})", request.remote_addr)
        return send_file(resume_path, as_attachment=True, download_name=filename, mimetype=mimetype)
    else:
        flash(f'Resume file ({format}) not found.', 'error')
        return redirect(url_for('home'))

@app.route('/download-resume')
def download_resume_legacy():
    """Legacy download resume route (redirects to PDF)"""
    return redirect(url_for('download_resume', format='pdf'))

@app.route('/robots.txt')
def robots_txt():
    """Serve robots.txt for SEO"""
    return send_file('static/robots.txt', mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap_xml():
    """Generate and serve sitemap.xml for SEO"""
    try:
        # Get the base URL from the request
        base_url = request.url_root.rstrip('/')
        
        # Read the sitemap template
        sitemap_content = render_template('sitemap.xml')
        
        # Replace the placeholder with actual base URL
        sitemap_content = sitemap_content.replace('{{BASE_URL}}', base_url)
        
        # Create response with proper headers
        response = app.response_class(
            sitemap_content,
            mimetype='application/xml'
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating sitemap: {str(e)}")
        return "Sitemap temporarily unavailable", 500

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form"""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            subject = request.form.get('subject', '').strip()
            message = request.form.get('message', '').strip()
            
            # Validation
            required_fields = settings['contact_form']['required_fields']
            if not all([request.form.get(field, '').strip() for field in required_fields]):
                flash('Please fill in all required fields.', 'error')
                return render_template('contact.html')
            
            # Check message length
            max_length = settings['contact_form']['max_message_length']
            if len(message) > max_length:
                flash(f'Message too long. Maximum {max_length} characters allowed.', 'error')
                return render_template('contact.html')
            
            # Send email
            try:
                msg = Message(
                    subject=f"Portfolio Contact: {subject}",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[os.getenv('ADMIN_EMAIL')]
                )
                
                msg.html = f"""
                <h3>New Contact Form Submission</h3>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Subject:</strong> {subject}</p>
                <p><strong>Message:</strong></p>
                <p>{message.replace(chr(10), '<br>')}</p>
                <hr>
                <p><em>Sent from your portfolio website at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
                """
                
                mail.send(msg)
                
                logger.info(f"Contact form submitted by {email}")
                flash(settings['contact_form']['success_message'], 'success')
                return redirect(url_for('contact'))
                
            except Exception as e:
                logger.error(f"Error sending contact email: {str(e)}")
                flash(settings['contact_form']['error_message'], 'error')
                return render_template('contact.html')
                
        except Exception as e:
            logger.error(f"Error processing contact form: {str(e)}")
            flash('An unexpected error occurred. Please try again.', 'error')
            return render_template('contact.html')
    
    return render_template('contact.html')

@app.route('/contact-ajax', methods=['POST'])
def contact_ajax():
    """Handle contact form submission via AJAX"""
    try:
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        # Validation
        required_fields = settings['contact_form']['required_fields']
        if not all([request.form.get(field, '').strip() for field in required_fields]):
            return jsonify({
                'success': False,
                'message': 'Please fill in all required fields.'
            }), 400
        
        # Check message length
        max_length = settings['contact_form']['max_message_length']
        if len(message) > max_length:
            return jsonify({
                'success': False,
                'message': f'Message too long. Maximum {max_length} characters allowed.'
            }), 400
        
        # Send email
        try:
            msg = Message(
                subject=f"Portfolio Contact: {subject}",
                sender=app.config['MAIL_USERNAME'],
                recipients=[os.getenv('ADMIN_EMAIL')]
            )
            
            msg.html = f"""
            <h3>New Contact Form Submission</h3>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Subject:</strong> {subject}</p>
            <p><strong>Message:</strong></p>
            <p>{message.replace(chr(10), '<br>')}</p>
            <hr>
            <p><em>Sent from your portfolio website at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
            """
            
            mail.send(msg)
            
            logger.info(f"Contact form submitted by {email} via AJAX")
            return jsonify({
                'success': True,
                'message': 'Thank you for your message! I\'ll get back to you soon.'
            })
            
        except Exception as e:
            logger.error(f"Error sending contact email via AJAX: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'There was an error sending your message. Please try again later.'
            }), 500
            
    except Exception as e:
        logger.error(f"Error processing contact form via AJAX: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An unexpected error occurred. Please try again.'
        }), 500

# Admin routes
@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    # Mock statistics for dashboard
    stats = {
        'page_views': '1,234',
        'contact_messages': '12',
        'projects': '8',
        'last_updated': 'Today'
    }
    
    # System information
    import sys
    system_info = {
        'flask_version': '3.0.0',
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    }
    
    return render_template('admin/dashboard.html', stats=stats, **system_info)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        password = request.form.get('password', '')
        
        if security_manager.validate_admin_access(password):
            session['admin_authenticated'] = True
            session['admin_login_time'] = datetime.now().isoformat()
            log_admin_action("Admin login successful", request.remote_addr)
            return redirect(url_for('admin_dashboard'))
        else:
            log_security_event("Failed admin login", f"Invalid password from {request.remote_addr}", request)
            flash('Invalid password or password expired.', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    if 'admin_authenticated' in session:
        log_admin_action("Admin logout", request.remote_addr)
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

@app.route('/admin/edit/<section>')
@admin_required
def admin_edit_section(section):
    """Edit section content"""
    valid_sections = ['home', 'about', 'experience']
    if section not in valid_sections:
        flash('Invalid section.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    data = load_json_data(f'{section}.json')
    return render_template('admin/edit_section.html', section=section, data=data)

@app.route('/admin/save/<section>', methods=['POST'])
@admin_required
def admin_save_section(section):
    """Save section content"""
    valid_sections = ['home', 'about', 'experience']
    if section not in valid_sections:
        logger.warning(f"Invalid section attempted: {section}")
        return jsonify({'success': False, 'message': 'Invalid section'})
    
    try:
        data = request.get_json()
        if not data:
            logger.error("No JSON data received in request")
            return jsonify({'success': False, 'message': 'No data received'})
        
        logger.info(f"Attempting to save {section} content: {data}")
        
        # Save the file
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', f'{section}.json')
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        
        # Clear all cache
        cache.clear()
        
        # Verify the save worked
        with open(file_path, 'r') as f:
            saved_data = json.load(f)
        
        logger.info(f"Successfully saved and verified {section} content")
        log_admin_action(f"Updated {section} content", request.remote_addr)
        return jsonify({'success': True, 'message': 'Content saved successfully'})
        
    except Exception as e:
        logger.error(f"Error saving {section} content: {str(e)}")
        return jsonify({'success': False, 'message': f'An error occurred: {str(e)}'})

# Debug route to test file operations
@app.route('/admin/debug/test-save')
@admin_required
def debug_test_save():
    """Debug route to test file saving"""
    try:
        test_data = {"test": "data", "timestamp": datetime.now().isoformat()}
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'test.json')
        with open(file_path, 'w') as f:
            json.dump(test_data, f, indent=4)
        return jsonify({'success': True, 'message': 'Test file saved successfully', 'path': file_path})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Resume Management Routes
@app.route('/admin/upload-resume', methods=['POST'])
@admin_required
def upload_resume():
    """Upload resume files"""
    try:
        files_uploaded = []
        upload_folder = 'static/files'
        
        # Ensure upload directory exists
        os.makedirs(upload_folder, exist_ok=True)
        
        # Handle PDF file
        if 'pdfFile' in request.files:
            pdf_file = request.files['pdfFile']
            if pdf_file and pdf_file.filename:
                if pdf_file.content_type != 'application/pdf':
                    return jsonify({'success': False, 'message': 'PDF file must be in PDF format'})
                
                # Check file size by reading content
                pdf_content = pdf_file.read()
                if len(pdf_content) > 10 * 1024 * 1024:  # 10MB
                    return jsonify({'success': False, 'message': 'PDF file too large (max 10MB)'})
                
                pdf_path = os.path.join(upload_folder, 'resume.pdf')
                pdf_file.seek(0)  # Reset file pointer
                pdf_file.save(pdf_path)
                files_uploaded.append('resume.pdf')
                log_admin_action(f"Resume PDF uploaded", request.remote_addr)
        
        # Handle Word file
        if 'wordFile' in request.files:
            word_file = request.files['wordFile']
            if word_file and word_file.filename:
                if word_file.content_type not in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                    return jsonify({'success': False, 'message': 'Word file must be in DOC or DOCX format'})
                
                # Check file size by reading content
                word_content = word_file.read()
                if len(word_content) > 10 * 1024 * 1024:  # 10MB
                    return jsonify({'success': False, 'message': 'Word file too large (max 10MB)'})
                
                word_path = os.path.join(upload_folder, 'resume.docx')
                word_file.seek(0)  # Reset file pointer
                word_file.save(word_path)
                files_uploaded.append('resume.docx')
                log_admin_action(f"Resume Word document uploaded", request.remote_addr)
        
        if not files_uploaded:
            return jsonify({'success': False, 'message': 'No valid files uploaded'})
        
        return jsonify({
            'success': True, 
            'message': f'Successfully uploaded: {", ".join(files_uploaded)}',
            'files': files_uploaded
        })
        
    except Exception as e:
        logger.error(f"Resume upload error: {str(e)}")
        return jsonify({'success': False, 'message': f'Upload error: {str(e)}'})

@app.route('/admin/check-resume-files')
@admin_required
def check_resume_files():
    """Check what resume files are currently available"""
    try:
        files = []
        upload_folder = 'static/files'
        
        # Check for PDF
        pdf_path = os.path.join(upload_folder, 'resume.pdf')
        if os.path.exists(pdf_path):
            size = os.path.getsize(pdf_path)
            files.append({
                'name': 'resume.pdf',
                'type': 'pdf',
                'size': f"{size / (1024*1024):.1f} MB"
            })
        
        # Check for Word
        word_path = os.path.join(upload_folder, 'resume.docx')
        if os.path.exists(word_path):
            size = os.path.getsize(word_path)
            files.append({
                'name': 'resume.docx',
                'type': 'word',
                'size': f"{size / (1024*1024):.1f} MB"
            })
        
        return jsonify({'success': True, 'files': files})
        
    except Exception as e:
        logger.error(f"Check resume files error: {str(e)}")
        return jsonify({'success': False, 'message': f'Error checking files: {str(e)}'})

@app.route('/admin/delete-resume', methods=['POST'])
@admin_required
def delete_resume():
    """Delete a resume file"""
    try:
        data = request.get_json()
        filename = data.get('filename')
        
        if not filename or filename not in ['resume.pdf', 'resume.docx']:
            return jsonify({'success': False, 'message': 'Invalid filename'})
        
        file_path = os.path.join('static/files', filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            log_admin_action(f"Resume file deleted: {filename}", request.remote_addr)
            return jsonify({'success': True, 'message': f'{filename} deleted successfully'})
        else:
            return jsonify({'success': False, 'message': 'File not found'})
            
    except Exception as e:
        logger.error(f"Delete resume file error: {str(e)}")
        return jsonify({'success': False, 'message': f'Delete error: {str(e)}'})

# API routes
@app.route('/api/data/<section>')
def api_get_data(section):
    """Get section data as JSON"""
    valid_sections = ['home', 'about', 'experience']
    if section not in valid_sections:
        return jsonify({'error': 'Invalid section'}), 400
    
    data = load_json_data(f'{section}.json')
    return jsonify(data)

# Backup and Restore routes
@app.route('/admin/backup')
@admin_required
def admin_backup():
    """Create and download backup of all data"""
    try:
        import zipfile
        from io import BytesIO
        from datetime import datetime
        
        # Create a zip file in memory
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add JSON data files
            data_files = ['home.json', 'about.json', 'experience.json']
            for filename in data_files:
                file_path = os.path.join(BASE_DIR, 'data', filename)
                if os.path.exists(file_path):
                    zip_file.write(file_path, f'data/{filename}')
            
            # Add settings if exists
            settings_path = os.path.join(BASE_DIR, 'settings.json')
            if os.path.exists(settings_path):
                zip_file.write(settings_path, 'settings.json')
        
        zip_buffer.seek(0)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'portfolio_backup_{timestamp}.zip'
        
        log_admin_action(f"Data backup created: {filename}", request.remote_addr)
        
        return send_file(
            zip_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/zip'
        )
        
    except Exception as e:
        logger.error(f"Backup creation failed: {str(e)}")
        flash('Backup creation failed. Please try again.', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/restore', methods=['GET', 'POST'])
@admin_required
def admin_restore():
    """Restore data from backup"""
    if request.method == 'GET':
        return render_template('admin/restore.html')
    
    try:
        import zipfile
        
        if 'backup_file' not in request.files:
            flash('No file selected.', 'error')
            return redirect(url_for('admin_restore'))
        
        file = request.files['backup_file']
        if file.filename == '':
            flash('No file selected.', 'error')
            return redirect(url_for('admin_restore'))
        
        if not file.filename.endswith('.zip'):
            flash('Please upload a ZIP file.', 'error')
            return redirect(url_for('admin_restore'))
        
        # Create backup of current data before restore
        current_backup_dir = os.path.join(BASE_DIR, 'backups', 'pre_restore')
        os.makedirs(current_backup_dir, exist_ok=True)
        
        # Extract and restore files
        with zipfile.ZipFile(file, 'r') as zip_file:
            # Validate zip contents
            zip_contents = zip_file.namelist()
            
            for file_info in zip_file.infolist():
                if file_info.filename.startswith('data/') and file_info.filename.endswith('.json'):
                    # Extract to data directory
                    zip_file.extract(file_info, BASE_DIR)
                elif file_info.filename == 'settings.json':
                    # Extract settings file
                    zip_file.extract(file_info, BASE_DIR)
        
        log_admin_action(f"Data restored from backup: {file.filename}", request.remote_addr)
        flash('Data restored successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
        
    except Exception as e:
        logger.error(f"Restore failed: {str(e)}")
        flash('Restore failed. Please check the backup file and try again.', 'error')
        return redirect(url_for('admin_restore'))

@app.route('/admin/settings', methods=['GET', 'POST'])
@admin_required
def admin_settings():
    """Admin settings management"""
    if request.method == 'GET':
        return render_template('admin/settings.html')
    
    try:
        # Handle settings update
        action = request.form.get('action')
        
        if action == 'regenerate_password':
            # Force password regeneration
            new_password = security_manager.generate_new_password()
            if new_password:
                flash(f'New password generated and sent to your email: {new_password}', 'success')
                log_admin_action("Password manually regenerated", request.remote_addr)
            else:
                flash('Failed to generate new password.', 'error')
        
        elif action == 'update_email':
            new_email = request.form.get('admin_email')
            if new_email:
                # Update admin email in settings
                settings_path = os.path.join(BASE_DIR, 'settings.json')
                if os.path.exists(settings_path):
                    with open(settings_path, 'r') as f:
                        settings = json.load(f)
                    settings['admin_email'] = new_email
                    with open(settings_path, 'w') as f:
                        json.dump(settings, f, indent=2)
                    flash('Admin email updated successfully!', 'success')
                    log_admin_action(f"Admin email updated to: {new_email}", request.remote_addr)
                else:
                    flash('Settings file not found.', 'error')
        
        return redirect(url_for('admin_settings'))
        
    except Exception as e:
        logger.error(f"Settings update failed: {str(e)}")
        flash('Settings update failed. Please try again.', 'error')
        return redirect(url_for('admin_settings'))

if __name__ == '__main__':
    # Check if required environment variables are set
    required_env_vars = ['FLASK_SECRET_KEY', 'GMAIL_USERNAME', 'GMAIL_APP_PASSWORD', 'ADMIN_EMAIL']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error("Missing required environment variables:")
        for var in missing_vars:
            logger.error(f"  - {var}")
        logger.error("Please create a .env file based on .env.example and set these variables.")
        logger.error("Copy .env.example to .env and fill in your actual values.")
        exit(1)
    
    # Initialize security system
    if init_security_system():
        logger.info("Starting Portfolio Flask Application")
        
        # Get port from environment (for Heroku)
        port = int(os.getenv('PORT', 5000))
        
        app.run(
            host='0.0.0.0',
            port=port,
            debug=app.config['DEBUG']
        )
    else:
        logger.error("Failed to initialize security system. Exiting.")
        exit(1)