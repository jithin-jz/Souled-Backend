from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from products.models import Product
from orders.models import Order, Address
from cart.models import Cart, CartItem

User = get_user_model()


class OrderCreationTests(TestCase):
    """Test order creation flow"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Create user
        self.user = User.objects.create_user(
            email='user@test.com',
            password='testpass123'
        )
        
        # Create product
        self.product = Product.objects.create(
            name='Test Product',
            price=99.99,
            category='men',
            description='Test description',
            stock=10
        )
        
        # Create address
        self.address = Address.objects.create(
            user=self.user,
            full_name='Test User',
            phone='1234567890',
            street='123 Test St',
            city='Test City',
            pincode='123456'
        )
        
        self.client.force_authenticate(user=self.user)
    
    def test_create_cod_order(self):
        """Test creating a Cash on Delivery order"""
        data = {
            'cart': [
                {
                    'id': self.product.id,
                    'name': self.product.name,
                    'price': str(self.product.price),
                    'quantity': 2
                }
            ],
            'address_id': self.address.id,
            'payment_method': 'cod'
        }
        
        response = self.client.post('/api/orders/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['payment_method'], 'cod')
        self.assertEqual(response.data['payment_status'], 'unpaid')
        self.assertEqual(response.data['order_status'], 'processing')
    
    def test_create_order_with_insufficient_stock(self):
        """Test that order creation fails with insufficient stock"""
        data = {
            'cart': [
                {
                    'id': self.product.id,
                    'name': self.product.name,
                    'price': str(self.product.price),
                    'quantity': 100  # More than available stock
                }
            ],
            'address_id': self.address.id,
            'payment_method': 'cod'
        }
        
        response = self.client.post('/api/orders/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Insufficient stock', response.data['error'])
    
    def test_create_order_without_address(self):
        """Test that order creation fails without address"""
        data = {
            'cart': [
                {
                    'id': self.product.id,
                    'name': self.product.name,
                    'price': str(self.product.price),
                    'quantity': 1
                }
            ],
            'payment_method': 'cod'
        }
        
        response = self.client.post('/api/orders/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_authenticated_user_can_view_own_orders(self):
        """Test that users can view their own orders"""
        # Create an order first
        Order.objects.create(
            user=self.user,
            address=self.address,
            payment_method='cod',
            total_amount=99.99
        )
        
        response = self.client.get('/api/orders/my/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
