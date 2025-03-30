from datetime import datetime
from app.extensions import db

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_requests.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Review {self.id} by User {self.user_id} for Professional {self.professional_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'professional_id': self.professional_id,
            'service_request_id': self.service_request_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        } 