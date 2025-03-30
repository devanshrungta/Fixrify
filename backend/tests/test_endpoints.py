import requests
import json
from datetime import datetime, timedelta
import time

BASE_URL = "http://localhost:5000"

class TestEndpoints:
    def __init__(self):
        self.admin_token = None
        self.customer_token = None
        self.professional_token = None
        self.service_id = None
        self.service_request_id = None
        self.review_id = None

    def print_response(self, endpoint, response):
        """Helper to print response details"""
        print(f"\n{endpoint}:")
        print(f"Status Code: {response.status_code}")
        try:
            print(f"Response: {response.json()}")
        except:
            print(f"Raw Response: {response.text}")

    def setup(self):
        """Setup test data and get tokens"""
        print("\n=== Setting up test data ===")
        self.register_users()
        self.get_tokens()

    def register_users(self):
        """Register test users if they don't exist"""
        users = [
            {
                "email": "admin@example.com",
                "password": "admin123",
                "name": "Admin User",
                "role": "admin"
            },
            {
                "email": "customer@example.com",
                "password": "test123",
                "name": "Test Customer",
                "role": "customer"
            },
            {
                "email": "pro@example.com",
                "password": "test123",
                "name": "Test Professional",
                "role": "professional",
                "services": ["Plumbing", "Electrical"],
                "experience": 5,
                "about": "Experienced professional"
            }
        ]

        for user in users:
            try:
                response = requests.post(
                    f"{BASE_URL}/api/auth/register",
                    json=user
                )
                self.print_response(f"Register {user['role']}", response)
            except Exception as e:
                print(f"Exception while registering {user['role']}: {str(e)}")

    def get_tokens(self):
        """Get authentication tokens for different user roles"""
        print("\n=== Getting authentication tokens ===")
        
        # Admin login
        try:
            response = requests.post(
                f"{BASE_URL}/api/auth/login",
                json={
                    "email": "admin@example.com",
                    "password": "admin123"
                }
            )
            self.print_response("Admin login", response)
            if response.status_code == 200:
                self.admin_token = response.json()["access_token"]
        except Exception as e:
            print(f"Exception during admin login: {str(e)}")

        # Customer login
        try:
            response = requests.post(
                f"{BASE_URL}/api/auth/login",
                json={
                    "email": "customer@example.com",
                    "password": "test123"
                }
            )
            self.print_response("Customer login", response)
            if response.status_code == 200:
                self.customer_token = response.json()["access_token"]
        except Exception as e:
            print(f"Exception during customer login: {str(e)}")

        # Professional login
        try:
            response = requests.post(
                f"{BASE_URL}/api/auth/login",
                json={
                    "email": "pro@example.com",
                    "password": "test123"
                }
            )
            self.print_response("Professional login", response)
            if response.status_code == 200:
                self.professional_token = response.json()["access_token"]
        except Exception as e:
            print(f"Exception during professional login: {str(e)}")

    def test_auth_endpoints(self):
        """Test authentication endpoints"""
        print("\n=== Testing Auth Endpoints ===")
        
        # Test refresh token
        headers = {"Authorization": f"Bearer {self.customer_token}"}
        response = requests.post(f"{BASE_URL}/api/auth/refresh", headers=headers)
        self.print_response("Refresh token", response)

        # Test get profile
        response = requests.get(f"{BASE_URL}/api/auth/profile", headers=headers)
        self.print_response("Get profile", response)

        # Test update profile
        profile_data = {
            "name": "Updated Customer Name",
            "phone": "1234567890"
        }
        response = requests.put(f"{BASE_URL}/api/auth/profile", headers=headers, json=profile_data)
        self.print_response("Update profile", response)

    def test_admin_endpoints(self):
        """Test admin endpoints"""
        print("\n=== Testing Admin Endpoints ===")
        headers = {"Authorization": f"Bearer {self.admin_token}"}

        # Test dashboard
        response = requests.get(f"{BASE_URL}/api/admin/dashboard", headers=headers)
        self.print_response("Admin dashboard", response)

        # Test service management
        # Create service
        service_data = {
            "name": "Test Service",
            "description": "Test service description",
            "category": "General",
            "base_price": 100.0
        }
        response = requests.post(f"{BASE_URL}/api/admin/services", headers=headers, json=service_data)
        self.print_response("Create service", response)
        if response.status_code == 201:
            self.service_id = response.json()["id"]

        # Get all services
        response = requests.get(f"{BASE_URL}/api/admin/services", headers=headers)
        self.print_response("Get all services", response)

        # Update service
        if self.service_id:
            update_data = {"base_price": 120.0}
            response = requests.put(f"{BASE_URL}/api/admin/services/{self.service_id}", headers=headers, json=update_data)
            self.print_response("Update service", response)

        # Test professional management
        response = requests.get(f"{BASE_URL}/api/admin/professionals/pending", headers=headers)
        self.print_response("Get pending professionals", response)

        response = requests.get(f"{BASE_URL}/api/admin/professionals", headers=headers)
        self.print_response("Get all professionals", response)

        # Test user management
        response = requests.get(f"{BASE_URL}/api/admin/users", headers=headers)
        self.print_response("Get all users", response)

    def test_customer_endpoints(self):
        """Test customer endpoints"""
        print("\n=== Testing Customer Endpoints ===")
        headers = {"Authorization": f"Bearer {self.customer_token}"}

        # Test dashboard
        response = requests.get(f"{BASE_URL}/api/customer/dashboard", headers=headers)
        self.print_response("Customer dashboard", response)

        # Test service requests
        if self.service_id:
            # Create service request
            request_data = {
                "service_id": self.service_id,
                "preferred_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                "address": "123 Test St",
                "remarks": "Test service request"
            }
            response = requests.post(f"{BASE_URL}/api/service-requests", headers=headers, json=request_data)
            self.print_response("Create service request", response)
            if response.status_code == 201:
                self.service_request_id = response.json()["id"]

        # Get service requests
        response = requests.get(f"{BASE_URL}/api/customer/requests", headers=headers)
        self.print_response("Get customer requests", response)

        # Test cancel request
        if self.service_request_id:
            response = requests.post(f"{BASE_URL}/api/customer/requests/{self.service_request_id}/cancel", headers=headers)
            self.print_response("Cancel service request", response)

    def test_professional_endpoints(self):
        """Test professional endpoints"""
        print("\n=== Testing Professional Endpoints ===")
        headers = {"Authorization": f"Bearer {self.professional_token}"}

        # Test dashboard
        response = requests.get(f"{BASE_URL}/api/professional/dashboard", headers=headers)
        self.print_response("Professional dashboard", response)

        # Test service requests
        response = requests.get(f"{BASE_URL}/api/professional/requests", headers=headers)
        self.print_response("Get available requests", response)

        if self.service_request_id:
            # Accept request
            response = requests.post(
                f"{BASE_URL}/api/service-requests/{self.service_request_id}/accept",
                headers=headers
            )
            self.print_response("Accept service request", response)

            # Complete request
            complete_data = {"actual_price": 150.0}
            response = requests.post(
                f"{BASE_URL}/api/service-requests/{self.service_request_id}/complete",
                headers=headers,
                json=complete_data
            )
            self.print_response("Complete service request", response)

    def test_general_endpoints(self):
        """Test general endpoints"""
        print("\n=== Testing General Endpoints ===")

        # Test get services
        response = requests.get(f"{BASE_URL}/api/services")
        self.print_response("Get services", response)

        # Test get service by ID
        if self.service_id:
            response = requests.get(f"{BASE_URL}/api/services/{self.service_id}")
            self.print_response("Get service by ID", response)

        # Test get professionals
        response = requests.get(f"{BASE_URL}/api/professionals")
        self.print_response("Get professionals", response)

    def run_all_tests(self):
        """Run all tests in sequence"""
        self.setup()
        time.sleep(1)  # Give the server some time to process
        
        print("\nStarting tests...")
        self.test_auth_endpoints()
        time.sleep(1)
        
        self.test_admin_endpoints()
        time.sleep(1)
        
        self.test_customer_endpoints()
        time.sleep(1)
        
        self.test_professional_endpoints()
        time.sleep(1)
        
        self.test_general_endpoints()
        print("\nAll tests completed!")

if __name__ == "__main__":
    tester = TestEndpoints()
    tester.run_all_tests() 