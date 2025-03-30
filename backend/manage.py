from app import create_app, db
from app.models.user import User
from app.models.service import Service, ServiceRequest
from app.models.review import Review
from datetime import datetime, timedelta
import pytz
import random
import faker

# Set UTC timezone
UTC = pytz.timezone('Asia/Kolkata')
fake = faker.Faker()

# Create the app context
app = create_app()

# Mock data generation function
def add_mock_data():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Add Users (Admin, Customers, Professionals with varied attributes)
        users = []

        # Create Admin
        admin = User(
            name='Admin User',
            email='admin@fixrify.com',
            password='adminpassword',  # Password will be hashed
            role='admin',
            phone='1234567890'
        )
        users.append(admin)

        # Create diverse customers
        customers = [
            User(
                name=f'Customer {i}',
                email=f'customer{i}@fixrify.com',
                password=f'password{i}',  # Password will be hashed
                role='customer',
                phone=f'100000000{i}'
            ) for i in range(1, 11)  # 10 customers
        ]

        # Create diverse professionals
        professionals = [
            User(
                name=f'Professional {i}',
                email=f'professional{i}@fixrify.com',
                password=f'password{i}',  # Password will be hashed
                role='professional',
                phone=f'200000000{i}',
                services=["Plumbing", "Electrical", "Cleaning", "Carpentry", "Painting"][i % 5],  # Variety of services
                experience=5 + (i % 5),  # Random years of experience between 5 and 9
            ) for i in range(1, 11)  # 10 professionals
        ]

        # Add all users (customers, professionals, and admin) to the session
        db.session.add_all(users + customers + professionals)
        db.session.commit()

        # Add diverse services with different categories and prices
        services = [
            Service(name='Plumbing', category='Home Improvement', base_price=100.0),
            Service(name='Electrical', category='Home Improvement', base_price=150.0),
            Service(name='Cleaning', category='Housekeeping', base_price=50.0),
            Service(name='Carpentry', category='Furniture', base_price=120.0),
            Service(name='Painting', category='Home Improvement', base_price=80.0),
            Service(name='Gardening', category='Outdoor', base_price=60.0),
            Service(name='AC Repair', category='Electrical', base_price=200.0),
            Service(name='Roofing', category='Construction', base_price=300.0),
            Service(name='Locksmith', category='Security', base_price=90.0),
            Service(name='Pest Control', category='Housekeeping', base_price=70.0)
        ]

        db.session.add_all(services)
        db.session.commit()

        # Add service requests (many-to-many combinations of customers and professionals)
        service_requests = []
        for customer in customers:
            for service in services:
                # Randomly select a status
                status = random.choice(['pending', 'accepted', 'completed', 'cancelled'])

                # Set preferred_date to the current date (or simulate some random dates)
                preferred_date = datetime.now() - timedelta(days=random.randint(1, 30))  # Random date within the last 30 days

                # Create service request with random details (as an instance of ServiceRequest model)
                request = ServiceRequest(
                    customer_id=customer.id,
                    service_id=service.id,
                    professional_id=random.choice(professionals).id,
                    status=status,
                    address=fake.address(),
                    preferred_date=preferred_date,
                    notes=fake.text(max_nb_chars=200),
                    final_price=random.uniform(service.base_price, service.base_price + 100),
                    completed_at=None  # Set to None by default
                )

                # Logic for status and completed_at field
                if status == 'completed':
                    # Set completed_at to be after the preferred_date
                    completed_at = preferred_date + timedelta(days=random.randint(1, 7))  # Completed 1-7 days after preferred date
                    request.completed_at = completed_at

                service_requests.append(request)

        db.session.add_all(service_requests)
        db.session.commit()

        # Add reviews for each service request
        for service_request in service_requests:
            review = Review(
                user_id=service_request.customer_id,
                professional_id=service_request.professional_id,
                service_request_id=service_request.id,
                rating=random.randint(1, 5),  # Random rating from 1 to 5
                comment=fake.text(max_nb_chars=200),
                created_at=datetime.now(UTC)  # Use timezone-aware UTC time
            )
            db.session.add(review)

        db.session.commit()

        print("Mock data added successfully!")

if __name__ == "__main__":
    add_mock_data()
