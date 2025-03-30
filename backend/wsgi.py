from app import create_app
from app.extensions import db
from app.models import User, Service, ServiceRequest, Review
from werkzeug.security import generate_password_hash

app = create_app()

def init_db():
    with app.app_context():
        # Create tables
        db.create_all()

        # Check if admin user exists
        admin = User.query.filter_by(email=app.config['ADMIN_EMAIL']).first()
        if not admin:
            # Create admin user
            admin = User(
                name='Admin',
                email=app.config['ADMIN_EMAIL'],
                password_hash=generate_password_hash(app.config['ADMIN_PASSWORD']),
                role='admin',
                is_approved=True
            )
            db.session.add(admin)
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 