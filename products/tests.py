from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from products.models import Product

User = get_user_model()


class ProductPermissionTests(TestCase):
    """Test that product mutations require staff permissions"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Create regular user
        self.user = User.objects.create_user(
            email='user@test.com',
            password='testpass123'
        )
        
        # Create staff user
        self.staff_user = User.objects.create_user(
            email='staff@test.com',
            password='testpass123',
            is_staff=True
        )
        
        # Create a test product
        self.product = Product.objects.create(
            name='Test Product',
            price=99.99,
            category='men',
            description='Test description',
            stock=10
        )
    
    def test_regular_user_cannot_create_product(self):
        """Regular users should not be able to create products"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'name': 'New Product',
            'price': 49.99,
            'category': 'women',
            'description': 'New product description',
            'stock': 5
        }
        
        response = self.client.post('/api/products/create/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_staff_user_can_create_product(self):
        """Staff users should be able to create products"""
        self.client.force_authenticate(user=self.staff_user)
        
        data = {
            'name': 'New Product',
            'price': 49.99,
            'category': 'women',
            'description': 'New product description',
            'stock': 5
        }
        
        response = self.client.post('/api/products/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_regular_user_cannot_update_product(self):
        """Regular users should not be able to update products"""
        self.client.force_authenticate(user=self.user)
        
        data = {'name': 'Updated Name'}
        response = self.client.patch(f'/api/products/{self.product.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_staff_user_can_update_product(self):
        """Staff users should be able to update products"""
        self.client.force_authenticate(user=self.staff_user)
        
        data = {'name': 'Updated Name'}
        response = self.client.patch(f'/api/products/{self.product.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_regular_user_cannot_delete_product(self):
        """Regular users should not be able to delete products"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_staff_user_can_delete_product(self):
        """Staff users should be able to delete products"""
        self.client.force_authenticate(user=self.staff_user)
        
        response = self.client.delete(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_anyone_can_view_product(self):
        """Anyone should be able to view product details"""
        # Test without authentication
        response = self.client.get(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test with regular user
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
