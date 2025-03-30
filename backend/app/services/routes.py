from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Service, ServiceRequest, User, Review
from app import db
from sqlalchemy import or_
from datetime import datetime
import logging
from app.services import bp
from sqlalchemy import func

logger = logging.getLogger(__name__)

@bp.route('/', methods=['GET', 'OPTIONS'])
def get_services():
    """Get all active services with average rating."""
    # Query services along with the average rating
    services = db.session.query(
        Service,
        func.avg(Review.rating).label('average_rating')  # Calculate the average rating
    ).outerjoin(Review, Service.id == Review.service_request_id)  # Left join with the Review table
    services = services.filter(Service.is_active == True)  # Filter for active services
    services = services.group_by(Service.id).all()  # Group by Service id to calculate the average
    
    # Prepare the response with services and average rating
    result = []
    for service, avg_rating in services:
        service_dict = service.to_dict()  # Get the service details as a dictionary
        service_dict['average_rating'] = avg_rating if avg_rating is not None else 0  # Add average rating
        result.append(service_dict)

    logger.debug(f'Found {len(result)} active services with average ratings')
    return jsonify(result)

@bp.route('/test', methods=['GET'])
def test():
    """Test endpoint."""
    return jsonify({'message': 'Services blueprint is working!'})

@bp.route('/<int:service_id>', methods=['GET', 'OPTIONS'])
def get_service(service_id):
    """Get a specific service by ID."""
    if request.method == 'OPTIONS':
        return '', 200
    try:
        service = Service.query.get_or_404(service_id)
        if not service.is_active:
            return jsonify({'error': 'Service not found'}), 404
        return jsonify(service.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/search', methods=['GET', 'OPTIONS'])
def search_services():
    """Search services by category."""
    if request.method == 'OPTIONS':
        return '', 200
    try:
        category = request.args.get('category')
        query = Service.query.filter_by(is_active=True)
        
        if category:
            query = query.filter_by(category=category)
        
        services = query.all()
        return jsonify([service.to_dict() for service in services])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/categories', methods=['GET', 'OPTIONS'])
def get_categories():
    """Get all unique service categories."""
    if request.method == 'OPTIONS':
        return '', 200
    try:
        categories = db.session.query(Service.category).distinct().all()
        return jsonify([category[0] for category in categories])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/book', methods=['POST', 'OPTIONS'])
@jwt_required()
def book_service():
    """Book a service."""
    if request.method == 'OPTIONS':
        return '', 200
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        # Validate required fields
        required_fields = ['service_id', 'preferred_date', 'preferred_time']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Check if service exists and is active
        service = Service.query.get_or_404(data['service_id'])
        if not service.is_active:
            return jsonify({'error': 'Service is not available'}), 400

        # Create booking
        booking = ServiceRequest(
            service_id=data['service_id'],
            user_id=current_user_id,
            preferred_date=datetime.strptime(data['preferred_date'], '%Y-%m-%d').date(),
            preferred_time=data['preferred_time'],
            notes=data.get('notes')
        )

        db.session.add(booking)
        service.total_bookings += 1
        db.session.commit()

        return jsonify({
            'message': 'Service booked successfully',
            'booking': booking.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/bookings', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_user_bookings():
    """Get all bookings for the current user."""
    if request.method == 'OPTIONS':
        return '', 200
    try:
        current_user_id = get_jwt_identity()
        bookings = ServiceRequest.query.filter_by(user_id=current_user_id).all()
        return jsonify([booking.to_dict() for booking in bookings])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/bookings/<int:booking_id>', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_booking(booking_id):
    """Get a specific booking by ID."""
    if request.method == 'OPTIONS':
        return '', 200
    try:
        current_user_id = get_jwt_identity()
        booking = ServiceRequest.query.filter_by(
            id=booking_id,
            user_id=current_user_id
        ).first_or_404()
        return jsonify(booking.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/requests', methods=['POST'])
@jwt_required()
def create_service_request():
    """Create a new service request."""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        required_fields = ['service_id', 'preferred_date', 'preferred_time', 'address']
        
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        service = Service.query.get_or_404(data['service_id'])
        if not service.is_active:
            return jsonify({'error': 'Service is not available'}), 400

        service_request = ServiceRequest(
            service_id=data['service_id'],
            user_id=current_user_id,
            preferred_date=datetime.strptime(data['preferred_date'], '%Y-%m-%d').date(),
            preferred_time=data['preferred_time'],
            address=data['address'],
            notes=data.get('remarks', '')
        )
        
        db.session.add(service_request)
        db.session.commit()

        return jsonify({
            'message': 'Service request created successfully',
            'id': service_request.id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/requests/<int:request_id>', methods=['PUT'])
@jwt_required()
def update_service_request(request_id):
    """Update a service request."""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        service_request = ServiceRequest.query.get_or_404(request_id)
        
        # Check if user is authorized to update the request
        if service_request.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()
        
        if 'status' in data:
            service_request.status = data['status']

        if 'remarks' in data:
            service_request.notes = data['remarks']

        if data.get('status') == 'completed':
            service_request.completion_date = datetime.utcnow()

        db.session.commit()
        return jsonify({'message': 'Service request updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/requests/<int:request_id>', methods=['GET'])
@jwt_required()
def get_service_request(request_id):
    """Get a specific service request."""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        service_request = ServiceRequest.query.get_or_404(request_id)
        
        # Check if user is authorized to view the request
        if service_request.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        return jsonify(service_request.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500 