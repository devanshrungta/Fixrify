from flask import Blueprint, request, jsonify, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Service, ServiceRequest, Review
from app import db
from app.auth.routes import role_required
from datetime import datetime
from app.customer import bp
from sqlalchemy import func

@bp.route('/test', methods=['GET'])
@role_required(['customer'])
def test():
    """Test endpoint."""
    return jsonify({'message': 'Customer blueprint is working!'})

@bp.route('/dashboard', methods=['GET'])
@role_required(['customer'])
def get_dashboard():
    """Get customer's dashboard data."""
    try:
        current_user_id = get_jwt_identity()
        customer = User.query.get_or_404(current_user_id)
        
        # Get customer's service requests
        active_requests = ServiceRequest.query.filter_by(
            customer_id=customer.id
        ).filter(ServiceRequest.status.in_(['pending', 'accepted'])).all()
        print(active_requests,"===================================")
        
        completed_requests = ServiceRequest.query.filter_by(
            customer_id=customer.id,
            status='completed'
        ).all()
        print(completed_requests,"===================================")
        
        # Get recent services
        recent_services = Service.query.filter_by(is_active=True).limit(5).all()
        print(recent_services,"===================================")
        
        return jsonify({
            'profile': customer.to_dict(),
            'stats': {
                'active_requests': len(active_requests),
                'completed_requests': len(completed_requests)
            },
            'active_requests': [req.to_dict() for req in active_requests],
            'completed_requests': [req.to_dict() for req in completed_requests],
            'recent_services': [service.to_dict() for service in recent_services]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/services/request', methods=['POST'])
@role_required(['customer'])
def request_service():
    """Request a new service."""
    try:
        current_user_id = get_jwt_identity()
        customer = User.query.get_or_404(current_user_id)
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['service_id', 'preferred_date', 'address']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get service details
        service = Service.query.get_or_404(data['service_id'])
        if not service.is_active:
            return jsonify({'error': 'Service is not available'}), 400
        
        # Create service request
        service_request = ServiceRequest(
            customer_id=customer.id,
            service_id=service.id,
            professional_id = data.get('professional_id'),
            status='pending',
            address=data['address'],
            preferred_date=datetime.strptime(data['preferred_date'], '%Y-%m-%d'),
            notes=data.get('description'),
            final_price =data.get('price')
        )
        
        db.session.add(service_request)
        db.session.commit()
        
        flash('Service request created successfully!', 'success')
        return jsonify(service_request.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/requests/<int:id>', methods=['PUT'])
@role_required(['customer'])
def update_request_service(id):
    """Update service."""
    try:
        current_user_id = get_jwt_identity()
        customer = User.query.get_or_404(current_user_id)
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['preferred_date', 'address']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get service details
        service = ServiceRequest.query.get_or_404(id)
        if not service:
            return jsonify({'error': "Service Request doesn't exist"}), 400
        
        service.address = data['address']
        service.description = data['description']
        service.preferred_date = datetime.strptime(data['preferred_date'], '%Y-%m-%d')
        service.final_price = data['price']
        service.professional_id = data['professional_id']
        
        db.session.commit()
        
        flash('Service request created successfully!', 'success')
        return jsonify(service.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/requests', methods=['GET'])
@role_required(['customer'])
def get_requests():
    """Get customer's service requests."""
    try:
        current_user_id = get_jwt_identity()
        status = request.args.get('status')
        
        query = ServiceRequest.query.filter_by(customer_id=current_user_id)
        if status:
            query = query.filter_by(status=status)
            
        requests = query.order_by(ServiceRequest.created_at.desc()).all()
        return jsonify([req.to_dict() for req in requests])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/requests/<int:request_id>/cancel', methods=['GET'])
@role_required(['customer'])
def cancel_request(request_id):
    """Cancel a service request."""
    try:
        current_user_id = get_jwt_identity()
        service_request = ServiceRequest.query.filter_by(
            id=request_id,
            customer_id=current_user_id
        ).first_or_404()
        
        if service_request.status not in ['pending', 'accepted']:
            return jsonify({'error': 'Cannot cancel this request'}), 400
        
        service_request.status = 'cancelled'
        service_request.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Service request cancelled successfully!', 'success')
        return jsonify(service_request.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/reviews', methods=['POST'])
@role_required(['customer'])
def add_review():
    """Add a review for a completed service."""
    try:
        data = request.get_json()
        if 'rating' not in data or 'comment' not in data:
            return jsonify({'error': 'Rating and comment are required'}), 400

        current_user_id = get_jwt_identity()
        service_request = ServiceRequest.query.filter_by(
            id=data['service_request_id'],
            customer_id=current_user_id,
            status='completed'
        ).first_or_404()
        
        existing_review = Review.query.filter_by(service_request_id=data['service_request_id']).first()
        # Check if already reviewed
        if existing_review:
            existing_review.rating=data['rating']
            existing_review.comment=data['comment']
        
        else:
            review = Review(
                user_id=current_user_id,
                professional_id=data['professional_id'],
                service_request_id=data['service_request_id'],
                rating=data['rating'],
                comment=data['comment']
            )
            db.session.add(review)
            
        # Update professional's rating
        professional = User.query.get(service_request.professional_id)
        professional.update_rating()
        
        db.session.commit()
        flash('Review added successfully!', 'success')
        return "Successfully review given", 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/profile', methods=['GET'])
@role_required(['customer'])
def get_profile():
    """Get customer's profile."""
    try:
        current_user_id = get_jwt_identity()
        customer = User.query.get_or_404(current_user_id)
        return jsonify(customer.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/profile', methods=['PUT'])
@role_required(['customer'])
def update_profile():
    """Update customer's profile."""
    try:
        current_user_id = get_jwt_identity()
        customer = User.query.get_or_404(current_user_id)
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = ['name', 'phone', 'address']
        for field in allowed_fields:
            if field in data:
                setattr(customer, field, data[field])
                
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return jsonify(customer.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 

@bp.route('/professionals/<int:serviceID>')
@role_required(['customer'])
def get_professionals(serviceID):
    try:
        # Get the service based on the serviceID
        service = Service.query.get(serviceID)
        if not service:
            return jsonify({'error': 'Service not found'}), 404
        print(service.name, '=================')

        # Get all professionals
        professionals = User.query.filter(
            User.role == 'professional',
            User.is_approved == 1
        ).all()

        # Filter professionals in Python
        filtered_professionals = [
            prof for prof in professionals if service.name in prof.services
        ]

        print(filtered_professionals, '=============================')
        
        if not filtered_professionals:
            return jsonify({'message': 'No professionals found for this service'}), 404

        return jsonify({
            'professionals': [prof.to_dict() for prof in filtered_professionals]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/stats', methods=['GET'])
@role_required(['customer'])
def get_customer_stats():
    """Get stats for customer's total requests, completed services, and reviews given."""
    try:
        # Get current customer by JWT identity
        current_user_id = get_jwt_identity()
        customer = User.query.get_or_404(current_user_id)

        # Total requests (all statuses)
        total_requests = ServiceRequest.query.filter_by(customer_id=customer.id).count()

        # Completed services (status='completed')
        completed_services = ServiceRequest.query.filter_by(
            customer_id=customer.id,
            status='completed'
        ).count()

        # Reviews given by the customer
        reviews_given = Review.query.filter_by(user_id=customer.id).count()

        # Return stats as JSON response
        return jsonify({
            'total_requests': total_requests,
            'completed_services': completed_services,
            'reviews_given': reviews_given
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
