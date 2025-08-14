from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database.database import SessionLocal
from models.models import User
import datetime
import os
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    # Remove all non-digit characters
    cleaned_phone = re.sub(r'\D', '', phone)
    # Check if it's a valid length (10-15 digits)
    return len(cleaned_phone) >= 10 and len(cleaned_phone) <= 15

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    db = SessionLocal()
    
    try:
        # Validate required fields - support both 'email' and 'emailOrPhone'
        required_fields = ['firstName', 'lastName', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Support both 'email' and 'emailOrPhone' for compatibility
        email_or_phone = data.get('email') or data.get('emailOrPhone')
        if not email_or_phone:
            return jsonify({'error': 'Email is required'}), 400
        
        # Validate email or phone
        is_email = validate_email(email_or_phone)
        is_phone = validate_phone(email_or_phone)
        
        if not is_email and not is_phone:
            return jsonify({'error': 'Please provide a valid email or phone number'}), 400
        
        # Check if user already exists
        existing_user = None
        if is_email:
            existing_user = db.query(User).filter(User.email == email_or_phone).first()
        else:
            existing_user = db.query(User).filter(User.phone == email_or_phone).first()
        
        if existing_user:
            return jsonify({'error': 'User already exists with this email or phone number'}), 409
        
        # Validate password strength
        password = data['password']
        if len(password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters long'}), 400
        
        # Create new user
        user = User(
            first_name=data['firstName'],
            last_name=data['lastName'],
            email=email_or_phone if is_email else None,
            phone=email_or_phone if is_phone else None,
            password_hash=generate_password_hash(password)
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Generate token using Flask-JWT-Extended
        token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=24))
        
        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'email': user.email,
                'phone': user.phone,
                'createdAt': user.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    
    finally:
        db.close()

@auth_bp.route('/signin', methods=['POST'])
def signin():
    data = request.json
    db = SessionLocal()
    
    try:
        print(f"Signin attempt with data: {data}")  # Debug logging
        
        # Support both 'email' and 'emailOrPhone' for compatibility
        email_or_phone = data.get('email') or data.get('emailOrPhone')
        password = data.get('password')
        
        print(f"Email/Phone: {email_or_phone}, Password provided: {bool(password)}")  # Debug logging
        
        if not email_or_phone or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user by email or phone
        is_email = validate_email(email_or_phone)
        
        print(f"Is email: {is_email}")  # Debug logging
        
        user = None
        if is_email:
            user = db.query(User).filter(User.email == email_or_phone).first()
            print(f"Looking for user by email: {email_or_phone}, found: {bool(user)}")
        else:
            user = db.query(User).filter(User.phone == email_or_phone).first()
            print(f"Looking for user by phone: {email_or_phone}, found: {bool(user)}")
        
        if not user:
            print("User not found")
            return jsonify({'error': 'Invalid credentials'}), 401
            
        if not check_password_hash(user.password_hash, password):
            print("Password check failed")
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Update last login
        user.last_login = datetime.datetime.utcnow()
        db.commit()
        
        # Generate token using Flask-JWT-Extended
        token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=24))
        
        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'email': user.email,
                'phone': user.phone,
                'createdAt': user.created_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        db.close()

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user info from token"""
    current_user_id = get_jwt_identity()
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.id == current_user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': user.id,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'email': user.email,
                'phone': user.phone,
                'createdAt': user.created_at.isoformat(),
                'lastLogin': user.last_login.isoformat() if user.last_login else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user (client-side token removal)"""
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Send password reset email"""
    data = request.json
    db = SessionLocal()
    
    try:
        email = data.get('email')
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        if not validate_email(email):
            return jsonify({'error': 'Please provide a valid email address'}), 400
        
        # Find user by email
        user = db.query(User).filter(User.email == email).first()
        if not user:
            # Don't reveal if email exists or not for security
            return jsonify({'message': 'If this email is registered, you will receive reset instructions'}), 200
        
        # Generate reset token (in production, use a more secure method with expiration)
        import secrets
        reset_token = secrets.token_urlsafe(32)
        
        # Store reset token (you might want to add a reset_token field to User model)
        # For now, we'll use a simple in-memory store (replace with database in production)
        if not hasattr(forgot_password, 'reset_tokens'):
            forgot_password.reset_tokens = {}
        
        forgot_password.reset_tokens[reset_token] = {
            'user_id': user.id,
            'email': email,
            'expires': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        
        # In production, send email with reset link
        # For development, return the reset token
        reset_url = f"http://localhost:5174/reset-password?token={reset_token}"
        
        print(f"🔐 PASSWORD RESET REQUEST:")
        print(f"📧 Email: {email}")
        print(f"🔗 Reset URL: {reset_url}")
        print(f"⏰ Token expires in 1 hour")
        
        return jsonify({
            'message': 'Password reset instructions sent to your email',
            'reset_url': reset_url  # Remove this in production
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset password with token"""
    data = request.json
    db = SessionLocal()
    
    try:
        token = data.get('token')
        new_password = data.get('password')
        
        if not token or not new_password:
            return jsonify({'error': 'Token and new password are required'}), 400
        
        # Validate password strength
        if len(new_password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters long'}), 400
        
        # Check if token exists and is valid
        if not hasattr(forgot_password, 'reset_tokens') or token not in forgot_password.reset_tokens:
            return jsonify({'error': 'Invalid or expired reset token'}), 400
        
        token_data = forgot_password.reset_tokens[token]
        
        # Check if token is expired
        if datetime.datetime.utcnow() > token_data['expires']:
            del forgot_password.reset_tokens[token]
            return jsonify({'error': 'Reset token has expired'}), 400
        
        # Find user
        user = db.query(User).filter(User.id == token_data['user_id']).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Update password
        user.password_hash = generate_password_hash(new_password)
        user.last_login = datetime.datetime.utcnow()
        db.commit()
        
        # Remove used token
        del forgot_password.reset_tokens[token]
        
        print(f"✅ PASSWORD RESET SUCCESSFUL:")
        print(f"📧 Email: {user.email}")
        print(f"🕒 Reset time: {datetime.datetime.utcnow()}")
        
        # Generate new login token
        login_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=24))
        
        return jsonify({
            'message': 'Password reset successful',
            'token': login_token,
            'user': {
                'id': user.id,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'email': user.email,
                'phone': user.phone,
                'createdAt': user.created_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()
