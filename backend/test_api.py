import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:5000/api'

def test_auth_endpoints():
    print("\nTesting Authentication Endpoints:")
    
    # Test registration
    print("\n1. Testing Registration:")
    register_data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'test123',
        'role': 'customer'
    }
    response = requests.post(f'{BASE_URL}/auth/register', json=register_data)
    print(f"Register Response: {response.status_code}")
    print(response.json())

    # Test login
    print("\n2. Testing Login:")
    login_data = {
        'email': 'test@example.com',
        'password': 'test123'
    }
    response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
    print(f"Login Response: {response.status_code}")
    print(response.json())
    
    if response.status_code == 200:
        return response.json()['access_token']
    return None

def test_service_endpoints(admin_token):
    print("\nTesting Service Endpoints:")
    headers = {'Authorization': f'Bearer {admin_token}'}

    # Test create service
    print("\n1. Testing Create Service:")
    service_data = {
        'name': 'Test Service',
        'description': 'Test service description',
        'category': 'Test Category',
        'base_price': 100.0
    }
    response = requests.post(f'{BASE_URL}/admin/services', headers=headers, json=service_data)
    print(f"Create Service Response: {response.status_code}")
    print(response.json())

    # Test get services
    print("\n2. Testing Get Services:")
    response = requests.get(f'{BASE_URL}/services')
    print(f"Get Services Response: {response.status_code}")
    print(response.json())

    return response.json()[0]['id'] if response.json() else None

def test_service_request_endpoints(customer_token, service_id):
    print("\nTesting Service Request Endpoints:")
    headers = {'Authorization': f'Bearer {customer_token}'}

    # Test create service request
    print("\n1. Testing Create Service Request:")
    request_data = {
        'service_id': service_id,
        'address': 'Test Address',
        'preferred_date': datetime.utcnow().isoformat(),
        'remarks': 'Test remarks'
    }
    response = requests.post(f'{BASE_URL}/service-requests', headers=headers, json=request_data)
    print(f"Create Service Request Response: {response.status_code}")
    print(response.json())

    # Test get service requests
    print("\n2. Testing Get Service Requests:")
    response = requests.get(f'{BASE_URL}/service-requests', headers=headers)
    print(f"Get Service Requests Response: {response.status_code}")
    print(response.json())

def test_admin_endpoints(admin_token):
    print("\nTesting Admin Endpoints:")
    headers = {'Authorization': f'Bearer {admin_token}'}

    # Test get dashboard
    print("\n1. Testing Get Dashboard:")
    response = requests.get(f'{BASE_URL}/admin/dashboard', headers=headers)
    print(f"Get Dashboard Response: {response.status_code}")
    print(response.json())

    # Test get users
    print("\n2. Testing Get Users:")
    response = requests.get(f'{BASE_URL}/admin/users', headers=headers)
    print(f"Get Users Response: {response.status_code}")
    print(response.json())

    # Test get professionals
    print("\n3. Testing Get Professionals:")
    response = requests.get(f'{BASE_URL}/admin/professionals', headers=headers)
    print(f"Get Professionals Response: {response.status_code}")
    print(response.json())

def main():
    # Test authentication endpoints and get tokens
    customer_token = test_auth_endpoints()
    
    # Create admin user and get admin token
    admin_data = {
        'name': 'Admin User',
        'email': 'admin@fixrify.com',
        'password': 'admin123',
        'role': 'admin'
    }
    requests.post(f'{BASE_URL}/auth/register', json=admin_data)
    admin_response = requests.post(f'{BASE_URL}/auth/login', json={'email': 'admin@fixrify.com', 'password': 'admin123'})
    admin_token = admin_response.json()['access_token']

    # Test service endpoints
    service_id = test_service_endpoints(admin_token)

    if service_id and customer_token:
        # Test service request endpoints
        test_service_request_endpoints(customer_token, service_id)

    # Test admin endpoints
    test_admin_endpoints(admin_token)

if __name__ == '__main__':
    main() 