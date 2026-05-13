"""
Expert System for Crop Recommendation
Main Flask Application with Authentication
"""
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from functools import wraps
from dotenv import load_dotenv
import os
import logging
import base64
from pathlib import Path
from modules.knowledge_base import KnowledgeBase
from modules.data_preprocessor import DataPreprocessor
from modules.inference_engine import InferenceEngine
from modules.classifier import CropClassifier
from modules.feedback_manager import FeedbackManager
from modules.auth_manager import AuthManager
from modules.history_manager import HistoryManager

load_dotenv()

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-2026')
app.config['SESSION_TYPE'] = 'filesystem'

# Create uploads directory for user photos
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize system modules
knowledge_base = KnowledgeBase()
preprocessor = DataPreprocessor()
inference_engine = InferenceEngine(knowledge_base)
classifier = CropClassifier()
feedback_manager = FeedbackManager()
auth_manager = AuthManager()
history_manager = HistoryManager()


# Decorator for login required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== HELPER FUNCTIONS ====================

def format_profile_data(user, history, stats):
    """Format user and history data for profile template"""
    if user and user.get('created_at'):
        user['created_at'] = str(user['created_at'])[:10]  # Convert to YYYY-MM-DD string
    
    if history:
        for record in history:
            if record.get('created_at'):
                record['created_at'] = str(record['created_at'])[:10]  # Convert to YYYY-MM-DD string
    
    return user, history, stats


# ==================== MAIN ROUTES ====================

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    """Home/Landing page"""
    return render_template('index.html')


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


# ==================== AUTHENTICATION ROUTES ====================

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        success, message, user_data = auth_manager.login_user(username, password)
        
        if success:
            session['user_id'] = user_data['id']
            session['username'] = user_data['username']
            session['email'] = user_data['email']
            logger.info(f"User logged in: {username}")
            return redirect(url_for('dashboard'))
        else:
            logger.warning(f"Login failed for user: {username}")
            return render_template('login.html', error=message)
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    """Registration page"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        location = request.form.get('location', '')
        soil_type = request.form.get('soil_type', '')
        farm_size = request.form.get('farm_size', '')
        
        # Validate passwords match
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')
        
        success, message, user_id = auth_manager.register_user(
            username, email, password, first_name, last_name
        )
        
        if success:
            logger.info(f"New user registered: {username}")
            return render_template('register.html', success='Registration successful! Please login.')
        else:
            return render_template('register.html', error=message)
    
    return render_template('register.html')


@app.route('/logout')
def logout():
    """Logout user"""
    username = session.get('username', 'Unknown')
    session.clear()
    logger.info(f"User logged out: {username}")
    return redirect(url_for('login_page'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Render the input dashboard"""
    user = auth_manager.get_user_by_id(session['user_id'])
    return render_template('dashboard.html', user=user)


@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    user = auth_manager.get_user_by_id(session['user_id'])
    history = history_manager.get_user_history(session['user_id'], limit=100)
    stats = history_manager.get_history_stats(session['user_id'])
    
    user, history, stats = format_profile_data(user, history, stats)
    return render_template('profile.html', user=user, history=history, stats=stats)


@app.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    """Update user profile including photo upload"""
    user_id = session['user_id']
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    location = request.form.get('location')
    soil_type = request.form.get('soil_type')
    farm_size = request.form.get('farm_size')
    photo_data = request.form.get('photo_data')  # Base64 encoded image data
    
    # Handle photo upload
    photo_url = None
    if photo_data and photo_data.startswith('data:image'):
        try:
            # Parse the base64 image data
            header, encoded = photo_data.split(',', 1)
            image_data = base64.b64decode(encoded)
            
            # Determine file extension from header
            extension = 'png'
            if 'jpeg' in header:
                extension = 'jpg'
            elif 'gif' in header:
                extension = 'gif'
            elif 'webp' in header:
                extension = 'webp'
            
            # Save the file
            filename = f"user_{user_id}_profile.{extension}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            photo_url = url_for('uploaded_file', filename=filename)
            logger.info(f"Photo uploaded for user {user_id}: {filename}")
            
            # Update session with new photo URL
            session['photo_url'] = photo_url
        except Exception as e:
            logger.error(f"Error processing photo upload: {str(e)}")
    
    # Update user profile with or without photo
    success, message = auth_manager.update_user_profile(
        user_id, first_name, last_name, location, soil_type, farm_size, photo_url
    )
    
    user = auth_manager.get_user_by_id(user_id)
    history = history_manager.get_user_history(user_id, limit=100)
    stats = history_manager.get_history_stats(user_id)
    user, history, stats = format_profile_data(user, history, stats)
    
    return render_template('profile.html', user=user, history=history, stats=stats, 
                          success=message if success else None, error=message if not success else None)


@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Change user password"""
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if new_password != confirm_password:
        user = auth_manager.get_user_by_id(session['user_id'])
        history = history_manager.get_user_history(session['user_id'], limit=100)
        stats = history_manager.get_history_stats(session['user_id'])
        user, history, stats = format_profile_data(user, history, stats)
        return render_template('profile.html', user=user, history=history, stats=stats,
                              error='Passwords do not match')
    
    success, message = auth_manager.change_password(session['user_id'], old_password, new_password)
    
    user = auth_manager.get_user_by_id(session['user_id'])
    history = history_manager.get_user_history(session['user_id'], limit=100)
    stats = history_manager.get_history_stats(session['user_id'])
    user, history, stats = format_profile_data(user, history, stats)
    
    return render_template('profile.html', user=user, history=history, stats=stats,
                          success=message if success else None, error=message if not success else None)


@app.route('/delete-history', methods=['POST'])
@login_required
def delete_history():
    """Delete a history record"""
    record_id = request.form.get('record_id')
    success, message = history_manager.delete_history_record(session['user_id'], record_id)
    
    user = auth_manager.get_user_by_id(session['user_id'])
    history = history_manager.get_user_history(session['user_id'], limit=100)
    stats = history_manager.get_history_stats(session['user_id'])
    user, history, stats = format_profile_data(user, history, stats)
    
    return render_template('profile.html', user=user, history=history, stats=stats,
                          success=message if success else None, error=message if not success else None)


# ==================== FILE SERVING ROUTES ====================
# ==================== FILE SERVING ROUTES ====================

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        logger.error(f"Error serving file {filename}: {str(e)}")
        return "File not found", 404


# ==================== API ROUTES ====================

@app.route('/api/recommend', methods=['POST'])
@app.route('/recommendation', methods=['POST'])
def recommendation_route():
    """
    Main recommendation endpoint
    Process: Input → Preprocess → Forward Chaining → ML Classification → Refine
    """
    try:
        return recommendation()
    except Exception as e:
        logger.error(f"Error processing recommendation: {str(e)}")
        return jsonify({'error': str(e)}), 400


def recommendation():
    try:
        data = request.json
        logger.info(f"Received input: {data}")

        # Step 1: Data Transformation/Preprocessing
        processed_data = preprocessor.preprocess(data)
        logger.info(f"Processed data: {processed_data}")

        # Step 2: Forward Chaining Rule Check
        rule_match = inference_engine.forward_chain(processed_data)

        if rule_match:
            primary_crop = rule_match['crop']
            confidence = rule_match['confidence']
            alternatives = rule_match['alternatives']
        else:
            # Step 3: ML Analysis using Bayesian Classification
            ml_prediction = classifier.predict(processed_data)
            primary_crop = ml_prediction['primary_crop']
            confidence = ml_prediction['confidence']
            alternatives = ml_prediction['alternatives']
            logger.info(f"ML Prediction: {primary_crop} with confidence {confidence}")

        # Step 4: Refinement with seasonal adjustments
        refined_recommendation = inference_engine.refine_recommendation(
            primary_crop, processed_data
        )

        recommendation = {
            'primary_crop': primary_crop,
            'confidence': round(confidence * 100, 2),
            'alternatives': alternatives,
            'reasoning': refined_recommendation.get('reasoning', ''),
            'seasonal_note': refined_recommendation.get('seasonal_note', '')
        }

        # Save to user history if a logged-in user exists
        user_id = session.get('user_id')
        if user_id is not None:
            history_manager.save_recommendation(user_id, data, recommendation)
        else:
            logger.warning("No active session found; skipping history save")

        logger.info(f"Recommendation: {recommendation}")
        return jsonify(recommendation), 200

    except Exception as e:
        logger.error(f"Error processing recommendation: {str(e)}")
        return jsonify({'error': str(e)}), 400


# ==================== OUTPUT PAGE ====================

@app.route('/output')
@login_required
def output_page():
    """Render the recommendation output page"""
    return render_template('output.html')


@app.route('/api/feedback', methods=['POST'])
@login_required
def submit_feedback():
    """
    Handle feedback submission
    Feedback types: 'accurate', 'somewhat_accurate', 'inaccurate'
    """
    try:
        feedback_data = request.json
        logger.info(f"Received feedback: {feedback_data}")
        
        # Store feedback
        feedback_manager.save_feedback(feedback_data)
        
        return jsonify({'message': 'Feedback recorded successfully'}), 200
    
    except Exception as e:
        logger.error(f"Error processing feedback: {str(e)}")
        return jsonify({'error': str(e)}), 400


@app.route('/api/crops', methods=['GET'])
@login_required
def get_crops():
    """Get list of all available crops with metadata"""
    try:
        crops = knowledge_base.get_all_crops()
        return jsonify(crops), 200
    except Exception as e:
        logger.error(f"Error fetching crops: {str(e)}")
        return jsonify({'error': str(e)}), 400


@app.route('/api/crop/<crop_name>', methods=['GET'])
@login_required
def get_crop_details(crop_name):
    """Get detailed information about a specific crop"""
    try:
        crop_info = knowledge_base.get_crop_info(crop_name)
        if crop_info:
            return jsonify(crop_info), 200
        else:
            return jsonify({'error': 'Crop not found'}), 404
    except Exception as e:
        logger.error(f"Error fetching crop details: {str(e)}")
        return jsonify({'error': str(e)}), 400


@app.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    """Delete user account"""
    user_id = session['user_id']
    username = session.get('username', 'Unknown')
    
    success, message = auth_manager.delete_user_account(user_id)
    
    if success:
        session.clear()
        logger.info(f"User account deleted: {username}")
        return redirect(url_for('index'))
    else:
        user = auth_manager.get_user_by_id(user_id)
        history = history_manager.get_user_history(user_id, limit=100)
        stats = history_manager.get_history_stats(user_id)
        return render_template('profile.html', user=user, history=history, stats=stats,
                              error=message)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Expert System is running'}), 200


if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=8080, use_reloader=False)
