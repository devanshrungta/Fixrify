from app.models.user import User
from app.models.service import Service, ServiceRequest
from app.models.review import Review

# Define table creation order
__all__ = [
    'User',
    'Service',
    'ServiceRequest',
    'Review'
]

# Import models to ensure they are registered with SQLAlchemy
from . import user, service 