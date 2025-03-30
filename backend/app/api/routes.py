from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import bp
from app.extensions import db
from app.models import User, Service, ServiceRequest
from datetime import datetime

@bp.route('/services', methods=['GET'])
def get_services():
    services = Service.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'description': s.description,
        'category': s.category,
        'base_price': s.base_price,
        'image_url': s.image_url
    } for s in services]), 200

@bp.route('/services/<int:id>', methods=['GET'])
def get_service(id):
    service = Service.query.get_or_404(id)
    return jsonify({
        'id': service.id,
        'name': service.name,
        'description': service.description,
        'category': service.category,
        'base_price': service.base_price,
        'image_url': service.image_url
    }), 200

@bp.route('/professionals', methods=['GET'])
def get_professionals():
    professionals = User.query.filter_by(role='professional', is_active=True, is_approved=True).all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'services': p.services,
        'experience': p.experience,
        'about': p.about,
        'average_rating': p.average_rating,
        'total_jobs': p.total_jobs
    } for p in professionals]), 200

@bp.route('/service-requests', methods=['POST'])
@jwt_required()
def create_service_request():
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    
    if user.role != 'customer':
        return jsonify({'error': 'Only customers can create service requests'}), 403
        
    data = request.get_json()
    
    # Parse the preferred_date string into a datetime object
    try:
        preferred_date = datetime.strptime(data['preferred_date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    service_request = ServiceRequest(
        customer_id=current_user_id,
        service_id=data['service_id'],
        address=data['address'],
        preferred_date=preferred_date,
        remarks=data.get('remarks')
    )
    
    db.session.add(service_request)
    db.session.commit()
    
    return jsonify({
        'message': 'Service request created successfully',
        'id': service_request.id
    }), 201

@bp.route('/service-requests', methods=['GET'])
@jwt_required()
def get_service_requests():
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    
    if user.role == 'customer':
        requests = ServiceRequest.query.filter_by(customer_id=current_user_id).all()
    elif user.role == 'professional':
        requests = ServiceRequest.query.filter_by(professional_id=current_user_id).all()
    else:
        return jsonify({'error': 'Invalid user role'}), 400
    
    return jsonify([{
        'id': r.id,
        'service': {
            'id': r.service.id,
            'name': r.service.name,
            'base_price': r.service.base_price
        },
        'customer': {
            'id': r.customer.id,
            'name': r.customer.name
        },
        'professional': {
            'id': r.professional.id,
            'name': r.professional.name
        } if r.professional else None,
        'status': r.status,
        'address': r.address,
        'preferred_date': r.preferred_date.isoformat() if r.preferred_date else None,
        'actual_price': r.actual_price,
        'remarks': r.remarks,
        'created_at': r.created_at.isoformat(),
        'completed_at': r.completed_at.isoformat() if r.completed_at else None
    } for r in requests]), 200

@bp.route('/service-requests/<int:id>/accept', methods=['POST'])
@jwt_required()
def accept_service_request(id):
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    
    if user.role != 'professional':
        return jsonify({'error': 'Only professionals can accept service requests'}), 403
    
    request = ServiceRequest.query.get_or_404(id)
    if request.status != 'pending':
        return jsonify({'error': 'Request is not in pending state'}), 400
    
    request.professional_id = current_user_id
    request.status = 'accepted'
    db.session.commit()
    
    return jsonify({'message': 'Service request accepted successfully'}), 200

@bp.route('/service-requests/<int:id>/complete', methods=['POST'])
@jwt_required()
def complete_service_request(id):
    current_user_id = get_jwt_identity()
    service_request = ServiceRequest.query.get_or_404(id)
    
    if service_request.professional_id != current_user_id:
        return jsonify({'error': 'Only assigned professional can complete the request'}), 403
    
    if service_request.status != 'accepted':
        return jsonify({'error': 'Request must be in accepted state'}), 400
    
    data = request.get_json()
    service_request.status = 'completed'
    service_request.actual_price = data.get('actual_price', service_request.service.base_price)
    service_request.completed_at = datetime.utcnow()
    
    # Update professional statistics
    professional = service_request.professional
    professional.total_jobs += 1
    
    db.session.commit()
    
    return jsonify({'message': 'Service request completed successfully'}), 200 