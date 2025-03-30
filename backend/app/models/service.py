from datetime import datetime
from app.extensions import db

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    base_price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    service_requests = db.relationship('ServiceRequest', backref='service', lazy='dynamic')

    def __repr__(self):
        return f'<Service {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'base_price': self.base_price,
            'image_url': self.image_url,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(20), default='pending')  # pending, accepted, completed, cancelled
    address = db.Column(db.String(255), nullable=False)
    preferred_date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text)
    final_price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    # Relationships
    reviews = db.relationship('Review', backref='service_request', lazy='dynamic')

    def __repr__(self):
        return f'<ServiceRequest {self.id}>'

    def to_dict(self):
        reviews = [review.to_dict() for review in self.reviews]
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'service_id': self.service_id,
            'professional_id': self.professional_id,
            'status': self.status,
            'address': self.address,
            'preferred_date': self.preferred_date,
            'notes': self.notes,
            'final_price': self.final_price,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'completed_at': self.completed_at,
            'service': self.service.to_dict() if self.service else None,
            'customer': self.customer.to_dict() if self.customer else None,
            'reviews': reviews,
            'professional': self.professional.to_dict() if self.professional else None
        }

    def complete(self, final_price=None):
        self.status = 'completed'
        self.completed_at = datetime.utcnow()
        if final_price:
            self.final_price = final_price
        db.session.commit()

    def cancel(self):
        self.status = 'cancelled'
        db.session.commit()

    def accept(self, professional_id):
        self.professional_id = professional_id
        self.status = 'accepted'
        db.session.commit() 