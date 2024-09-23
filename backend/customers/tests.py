from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Customer, RefreshToken
import jwt
import time

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.private_key = "gchvbnmpltfb3opmfnic4+54sff"

class CustomerTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        self.customer = Customer.objects.create(
            first_name="Test",
            last_name="Customer",
            date_of_birth="2000-01-01",
            phone_number="1234567890"
        )
    
    def test_get_customer_list(self):
        response = self.client.get('/customers/customer/')  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_customer_detail(self):
        response = self.client.get(f'/customers/customer/{self.customer.id}/') 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "Test")

    def test_get_customer_not_found(self):
        response = self.client.get('/customers/customer/999/')  
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_customer(self):
        data = {
            "first_name": "New",
            "last_name": "Customer",
            "date_of_birth": "1990-01-01",
            "phone_number": "0987654321"
        }
        response = self.client.post('/customers/customer/', data)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], "New")

    def test_update_customer(self):
        data = {
            "first_name": "Updated",
            "last_name": "Customer",
            "date_of_birth": "1995-05-05",
            "phone_number": "1122334455"
        }
        response = self.client.put(f'/customers/customer/{self.customer.id}/', data)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "Updated")

    def test_delete_customer(self):
        response = self.client.delete(f'/customers/customer/{self.customer.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Customer.objects.filter(id=self.customer.id).exists())
