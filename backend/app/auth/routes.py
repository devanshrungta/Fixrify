from flask import Blueprint, request, jsonify, current_app, flash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.models.user import User
from app import db
from datetime import timedelta, datetime
from config import Config
from app.auth import bp
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

def role_required(roles):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            if not user or user.role not in roles:
                return jsonify({'error': 'Unauthorized'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@bp.route('/test', methods=['GET'])
def test():
    """Test endpoint."""
    return jsonify({'message': 'Auth blueprint is working!'})

@bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create new user
    user = User(
        email=data['email'],
        name=data['name'],
        password=data['password'],  # This will use the password setter
        phone=data.get('phone'),
        role=data.get('role', 'customer')
    )
    
    if user.role == 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    # If user is a professional, set additional fields
    if user.role == 'professional':
        user.services = data.get('services', [])
        user.experience = data.get('experience')
        user.about = data.get('about')
        user.is_approved = False
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User registered successfully',
        'access_token': create_access_token(identity=user.id),
        'refresh_token': create_refresh_token(identity=user.id),
        'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'is_approved': user.is_approved
            }}), 201

@bp.route('/login', methods=['POST'])
def login():
    """Login user."""
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.verify_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'access_token': access_token,
            'refresh_token': create_refresh_token(identity=user.id),
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'is_approved': user.is_approved
            }
        }), 200
    
    return jsonify({'error': 'Invalid email or password'}), 401

@bp.route('/admin/login', methods=['POST'])
def admin_login():
    """Admin login."""
    try:
        response = request.get_json()
        data = response['email']
        print(data)
        
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password are required'}), 400
            
        print("email", data['email'])
        user = User.query.filter_by(email=data['email'], role='admin').first()
        print(user)

        if not user or not user.verify_password(data['password']):
            return jsonify({'error': 'Invalid admin credentials'}), 401
            
        if not user.is_active:
            return jsonify({'error': 'Admin account is disabled'}), 403
        
        # Update login info
        user.update_login_info(request.remote_addr)
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        flash('Admin login successful!', 'success')
        return jsonify({
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'is_approved': user.is_approved
            },
            'access_token': access_token,
            'refresh_token': refresh_token
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token."""
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    return jsonify({'access_token': access_token}), 200

@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile."""
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'phone': user.phone,
        'role': user.role,
        'is_approved': user.is_approved,
        'services': user.services if user.role == 'professional' else None,
        'experience': user.experience if user.role == 'professional' else None,
        'about': user.about if user.role == 'professional' else None,
        'average_rating': user.average_rating if user.role == 'professional' else None,
        'total_jobs': user.total_jobs if user.role == 'professional' else None
    }), 200

@bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile."""
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    data = request.get_json()
    
    # Update basic fields
    user.name = data.get('name', user.name)
    user.phone = data.get('phone', user.phone)
    
    # Update professional specific fields
    if user.role == 'professional':
        user.services = data.get('services', user.services)
        user.experience = data.get('experience', user.experience)
        user.about = data.get('about', user.about)
    
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return jsonify({'message': 'Profile updated successfully'}), 200

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify(user.to_dict()), 200 

@bp.route('/logout')
@jwt_required()
def logout():
    return jsonify({'message': 'User logged out successfully'}), 200