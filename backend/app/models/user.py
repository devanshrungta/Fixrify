from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models.review import Review

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), default='customer')  # admin, customer, professional
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    login_count = db.Column(db.Integer, default=0)

    # Professional specific fields
    services = db.Column(db.JSON)  # List of service categories
    experience = db.Column(db.Integer)  # Years of experience
    about = db.Column(db.Text)
    average_rating = db.Column(db.Float, default=0.0)
    total_jobs = db.Column(db.Integer, default=0)

    # Relationships
    customer_requests = db.relationship('ServiceRequest', 
                                      foreign_keys='ServiceRequest.customer_id',
                                      backref='customer',
                                      lazy='dynamic')
    professional_requests = db.relationship('ServiceRequest',
                                          foreign_keys='ServiceRequest.professional_id',
                                          backref='professional',
                                          lazy='dynamic')
    # Reviews given by this user
    reviews_given = db.relationship('Review',
                                  foreign_keys='Review.user_id',
                                  backref=db.backref('reviewer', lazy=True),
                                  lazy='dynamic')
    # Reviews received by this professional
    reviews_received = db.relationship('Review',
                                     foreign_keys='Review.professional_id',
                                     backref=db.backref('reviewed_professional', lazy=True),
                                     lazy='dynamic')

    def __repr__(self):
        return f'<User {self.email}>'

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role == 'professional':
            self.is_approved = False
        elif self.role == 'customer':
            self.is_approved = True

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_login_info(self, ip_address=None):
        self.last_login = datetime.utcnow()
        self.login_count += 1
        db.session.commit()

    def update_rating(self):
        reviews = self.reviews_received.all()
        if reviews:
            self.average_rating = sum(r.rating for r in reviews) / len(reviews)
            db.session.commit()
        else:
            self.average_rating = 0.0
            db.session.commit()

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'is_active': self.is_active,
            'is_approved': self.is_approved,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'last_login': self.last_login,
            'login_count': self.login_count
        }

        if self.role == 'professional':
            self.update_rating()
            data.update({
                'services': self.services,
                'experience': self.experience,
                'about': self.about,
                'average_rating': self.average_rating,
                'total_jobs': self.total_jobs
            })

        return data

    def is_admin(self):
        return self.role == 'admin'

    def is_professional(self):
        return self.role == 'professional'

    def is_customer(self):
        return self.role == 'customer'

    def can_accept_service(self, service_type):
        return self.is_professional() and service_type in self.services and self.is_approved

    def block(self):
        self.is_active = False
        db.session.commit()

    def unblock(self):
        self.is_active = True
        db.session.commit()

    def approve(self):
        if self.is_professional():
            self.is_approved = True
            db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password) 