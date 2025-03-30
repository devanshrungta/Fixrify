from flask import Blueprint, request, jsonify, flash, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Service, ServiceRequest
from app.extensions import db, cache
from functools import wraps
from app.admin import bp
from app.auth.routes import role_required
from app.decorators import admin_required
from app.tasks import generate_service_requests_csv
from datetime import datetime

from app.extensions import cache
from app.tasks import generate_service_requests_csv
from io import BytesIO
import csv

@bp.route('/test', methods=['GET'])
def test():
    """Test endpoint."""
    return jsonify({'message': 'Admin blueprint is working!'})

@bp.route('/dashboard', methods=['GET'])
@admin_required
@cache.cached()
def get_dashboard():
    total_users = User.query.count()
    total_professionals = User.query.filter_by(role='professional').count()
    total_customers = User.query.filter_by(role='customer').count()
    total_services = Service.query.count()
    total_requests = ServiceRequest.query.count()
    pending_requests = ServiceRequest.query.filter_by(status='pending').count()
    completed_requests = ServiceRequest.query.filter_by(status='completed').count()
    
    return jsonify({
        'total_users': total_users,
        'total_professionals': total_professionals,
        'total_customers': total_customers,
        'total_services': total_services,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'completed_requests': completed_requests
    }), 200

@bp.route('/services', methods=['GET'])
@admin_required
def get_services():
    """Get all services."""
    try:
        services = Service.query.all()
        return jsonify([service.to_dict() for service in services])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/services', methods=['POST'])
@admin_required
def create_service():
    data = request.get_json()
    service = Service(
        name=data['name'],
        description=data['description'],
        category=data['category'],
        base_price=data['price'],
        image_url=data.get('image_url')
    )
    db.session.add(service)
    db.session.commit()
    return jsonify({
        'message': 'Service created successfully',
        'id': service.id
    }), 201

@bp.route('/services/<int:id>', methods=['PUT'])
@admin_required
def update_service(id):
    service = Service.query.get_or_404(id)
    data = request.get_json()
    print(data.get('is_active'))
    
    service.name = data.get('name', service.name)
    service.description = data.get('description', service.description)
    service.category = data.get('category', service.category)
    service.base_price = data.get('price', service.base_price)
    service.image_url = data.get('image_url', service.image_url)
    service.is_active = data.get('is_active').lower() == 'true'
    print(service.is_active)
    
    db.session.commit()
    return jsonify({'message': 'Service updated successfully'}), 200

@bp.route('/services/<int:id>', methods=['DELETE'])
@admin_required
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    return jsonify({'message': 'Service deleted successfully'}), 200

@bp.route('/bookings', methods=['GET'])
@admin_required
def get_all_bookings():
    """Get all bookings."""
    try:
        status = request.args.get('status')
        query = ServiceRequest.query
        
        if status:
            query = query.filter_by(status=status)
            
        bookings = query.all()
        return jsonify([booking.to_dict() for booking in bookings])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/bookings/<int:booking_id>', methods=['PUT'])
@admin_required
def update_booking_status(booking_id):
    """Update booking status."""
    try:
        booking = ServiceRequest.query.get_or_404(booking_id)
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
            
        booking.status = data['status']
        db.session.commit()
        
        return jsonify(booking.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    """Get all users."""
    try:
        role = request.args.get('role')
        query = User.query
        
        if role:
            query = query.filter_by(role=role)
            
        users = query.all()
        return jsonify([user.to_dict() for user in users])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/users/<int:id>', methods=['PUT'])
@admin_required
def update_user(id):
    """Update a user's status."""
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)
    user.role = data.get('role', user.role)
    user.is_approved = data.get('is_approved', user.is_approved)

    db.session.commit()
    return jsonify(user.to_dict())

@bp.route('/users/<int:id>', methods=['DELETE'])
@admin_required
def delete_user(id):
    """Delete user."""
    user = User.query.get_or_404(id)
    db.session.delete(user)  # Mark the user for deletion
    db.session.commit()  # Commit the transaction to delete the user from the database
    return jsonify({'message': 'User deleted successfully'}), 200

@bp.route('/users', methods=['POST'])
@admin_required
def create_user():
    """Create new user."""
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
        is_active=data.get('is_active'),
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
    
    return jsonify({'message': 'User registered successfully'}), 201

@bp.route('/users/<int:id>/toggle-status', methods=['PUT'])
@admin_required
def toggle_status(id):
    """Update a user's status."""
    user = User.query.get_or_404(id)    
    user.is_approved = not user.is_approved
    db.session.commit()
    return jsonify(user.to_dict())
    
    return jsonify({'error': 'No status provided'}), 400

@bp.route('/professionals/pending', methods=['GET'])
@admin_required
def get_pending_professionals():
    try:
        # Get pending professionals
        pending_professionals = User.query.filter_by(role='professional', is_approved=False).all()

        return jsonify({
            'professionals': [prof.to_dict() for prof in pending_professionals]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/professionals', methods=['GET'])
@admin_required
def get_professionals():
    professionals = User.query.filter_by(role='professional').all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'email': p.email,
        'phone': p.phone,
        'services': p.services,
        'experience': p.experience,
        'about': p.about,
        'is_approved': p.is_approved,
        'average_rating': p.average_rating,
        'total_jobs': p.total_jobs
    } for p in professionals]), 200

@bp.route('/professionals/<int:id>/approve', methods=['POST'])
@admin_required
def approve_professional(id):
    professional = User.query.get_or_404(id)
    if professional.role != 'professional':
        return jsonify({'error': 'User is not a professional'}), 400
    
    professional.is_approved = True
    db.session.commit()
    return jsonify({'message': 'Professional approved successfully'}), 200

@bp.route('/professionals/<int:id>/block', methods=['POST'])
@admin_required
def block_professional(id):
    professional = User.query.get_or_404(id)
    if professional.role != 'professional':
        return jsonify({'error': 'User is not a professional'}), 400
    
    professional.is_active = False
    db.session.commit()
    return jsonify({'message': 'Professional blocked successfully'}), 200

@bp.route('/professionals/<int:id>/unblock', methods=['POST'])
@admin_required
def unblock_professional(id):
    professional = User.query.get_or_404(id)
    if professional.role != 'professional':
        return jsonify({'error': 'User is not a professional'}), 400
    
    professional.is_active = True
    db.session.commit()
    return jsonify({'message': 'Professional unblocked successfully'}), 200

@bp.route('/search/professionals', methods=['GET'])
@admin_required
def search_professionals():
    """Search professionals."""
    try:
        query = request.args.get('q', '')
        service_type = request.args.get('service_type')
        
        professionals = User.query.filter_by(role='professional')
        
        if query:
            professionals = professionals.filter(
                (User.name.ilike(f'%{query}%')) |
                (User.email.ilike(f'%{query}%'))
            )
            
        if service_type:
            professionals = professionals.filter(User.services.contains([service_type]))
            
        return jsonify([p.to_dict() for p in professionals.all()])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/exports/service-requests', methods=['POST'])
@admin_required
def export_service_requests():
    """Trigger CSV export generation for all service requests."""
    try:
        # Start async task to generate the CSV
        task = generate_service_requests_csv.delay()

        return jsonify({
            'message': 'CSV generation started.',
            'task_id': task.id  # Send the task ID to track progress or retrieve the file later
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/exports/<task_id>', methods=['GET'])
@admin_required
def get_export(task_id):
    """Retrieve the generated CSV export for service requests."""
    try:
        # Retrieve CSV data from the cache using task_id
        cache_key = f"service_requests_csv_{task_id}"
        csv_data = cache.get(cache_key)

        if not csv_data:
            return jsonify({'error': 'Export not found or expired'}), 404

        # Convert the CSV string data into bytes
        csv_bytes = csv_data.encode('utf-8')  # Encoding CSV data to bytes

        # Create an in-memory binary stream
        output = BytesIO(csv_bytes)
        output.seek(0)  # Rewind to the beginning of the file
        
        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name='service_requests.csv'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500
