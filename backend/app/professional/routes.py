from flask import Blueprint, request, jsonify, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, ServiceRequest, Service
from app import db
from app.auth.routes import role_required
from datetime import datetime
from app.professional import bp

@bp.route('/dashboard', methods=['GET'])
@role_required(['professional'])
def get_dashboard():
    """Get professional's dashboard data."""
    try:
        current_user_id = get_jwt_identity()
        professional = User.query.get_or_404(current_user_id)
        print("Found professional", professional)
        
        # Get pending requests for this professional's services
        pending_requests = ServiceRequest.query.filter_by(
            professional_id=professional.id,
            status='pending'
        ).all()
        
        # Get professional's accepted requests
        accepted_requests = ServiceRequest.query.filter_by(
            professional_id=professional.id,
            status='accepted'
        ).all()
        
        # Get completed services
        completed_services = ServiceRequest.query.filter_by(
            professional_id=professional.id,
            status='completed'
        ).all()
        
        return jsonify({
            'profile': professional.to_dict(),
            'stats': {
                'total_jobs': professional.total_jobs,
                'average_rating': professional.average_rating,
                'pending_requests': len(pending_requests),
                'active_requests': len(accepted_requests)
            },
            'pending_requests': [req.to_dict() for req in pending_requests],
            'active_requests': [req.to_dict() for req in accepted_requests],
            'completed_services': [req.to_dict() for req in completed_services]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/requests', methods=['GET'])
@role_required(['professional'])
def get_requests():
    """Get service requests for the professional."""
    try:
        current_user_id = get_jwt_identity()
        professional = User.query.get_or_404(current_user_id)
        
        status = request.args.get('status', 'pending')
        if status == 'pending':
            # Get requests matching professional's services
            requests = ServiceRequest.query.filter_by(
                professional_id=professional.id,
                status='pending'
            ).all()
        else:
            # Get requests assigned to this professional
            requests = ServiceRequest.query.filter_by(
                professional_id=professional.id,
                status=status
            ).all()
            
        return jsonify([req.to_dict() for req in requests])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/requests/<int:request_id>/accept', methods=['POST'])
@role_required(['professional'])
def accept_request(request_id):
    """Accept a service request."""
    try:
        current_user_id = get_jwt_identity()
        professional = User.query.get_or_404(current_user_id)
        service_request = ServiceRequest.query.get_or_404(request_id)
        
        # Validate request can be accepted
        if service_request.status != 'pending':
            return jsonify({'error': 'Request is not pending'}), 400
            
        # if service_request.service.category not in professional.services:
        #     return jsonify({'error': 'Service type mismatch'}), 400
            
        if not professional.is_approved:
            return jsonify({'error': 'Account not approved yet'}), 403
            
        # Accept the request
        service_request.professional_id = professional.id
        service_request.status = 'accepted'
        
        db.session.commit()
        flash('Service request accepted successfully!', 'success')
        return jsonify(service_request.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/requests/<int:request_id>/reject', methods=['POST'])
@role_required(['professional'])
def reject_request(request_id):
    """Reject a service request."""
    try:
        current_user_id = get_jwt_identity()
        professional = User.query.get_or_404(current_user_id)
        service_request = ServiceRequest.query.get_or_404(request_id)
        
        # Validate request can be rejected
        if service_request.status != 'pending':
            return jsonify({'error': 'Request is not pending'}), 400
            
        # if service_request.service.category not in professional.services:
        #     return jsonify({'error': 'Service type mismatch'}), 400
            
        # Reject the request
        service_request.status = 'rejected'
        service_request.notes = request.json.get('reason')
        
        db.session.commit()
        flash('Service request rejected successfully!', 'success')
        return jsonify(service_request.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/requests/<int:request_id>/complete', methods=['POST'])
@role_required(['professional'])
def complete_request(request_id):
    """Mark a service request as completed."""
    try:
        current_user_id = get_jwt_identity()
        professional = User.query.get_or_404(current_user_id)
        service_request = ServiceRequest.query.get_or_404(request_id)
        
        # Validate request can be completed
        if service_request.status != 'accepted':
            return jsonify({'error': 'Request is not accepted'}), 400
            
        if service_request.professional_id != professional.id:
            return jsonify({'error': 'Not assigned to this request'}), 403
            
        # Complete the request
        service_request.status = 'completed'
        service_request.completed_at = datetime.utcnow()
        
        # Update professional's stats
        professional.total_jobs += 1
        
        db.session.commit()
        flash('Service request completed successfully!', 'success')
        return jsonify(service_request.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/profile', methods=['GET'])
@role_required(['professional'])
def get_profile():
    """Get professional's profile."""
    try:
        current_user_id = get_jwt_identity()
        professional = User.query.get_or_404(current_user_id)
        return jsonify(professional.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/profile', methods=['PUT'])
@role_required(['professional'])
def update_profile():
    """Update professional's profile."""
    try:
        current_user_id = get_jwt_identity()
        professional = User.query.get_or_404(current_user_id)
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = ['name', 'phone', 'address', 'experience']
        for field in allowed_fields:
            if field in data:
                setattr(professional, field, data[field])
                
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return jsonify(professional.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 