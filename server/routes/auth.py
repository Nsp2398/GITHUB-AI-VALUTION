from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from database.database import SessionLocal
from models.models import User
import jwt
import datetime
import os
import re

auth_bp = Blueprint('auth', __name__)

def generate_token(user_id):
    """Generate JWT token for user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

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
        # Validate required fields
        required_fields = ['firstName', 'lastName', 'emailOrPhone', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate email or phone
        email_or_phone = data['emailOrPhone']
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
        
        # Generate token
        token = generate_token(user.id)
        
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
        
        # Validate required fields
        email_or_phone = data.get('emailOrPhone')
        password = data.get('password')
        
        print(f"Email/Phone: {email_or_phone}, Password provided: {bool(password)}")  # Debug logging
        
        if not email_or_phone or not password:
            return jsonify({'error': 'Email/phone and password are required'}), 400
        
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
        
        # Generate token
        token = generate_token(user.id)
        
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
def get_current_user():
    """Get current user info from token"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authorization token required'}), 401
    
    token = auth_header.split(' ')[1]
    db = SessionLocal()
    
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        user_id = payload['user_id']
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': user.id,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'email': user.email,
                'phone': user.phone,
                'createdAt': user.created_at.isoformat()
            }
        }), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        db.close()

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user (client-side token removal)"""
    return jsonify({'message': 'Logged out successfully'}), 200
