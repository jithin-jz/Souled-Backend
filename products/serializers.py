from rest_framework import serializers
from .models import Product
from utils import validate_price_range, validate_stock_quantity


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=255,
        min_length=3,
        error_messages={
            'required': 'Product name is required.',
            'min_length': 'Product name must be at least 3 characters.',
            'max_length': 'Product name cannot exceed 255 characters.',
        }
    )
    
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_price_range],
        error_messages={
            'required': 'Price is required.',
            'invalid': 'Price must be a valid number.',
            'max_digits': 'Price is too large.',
        }
    )
    
    stock = serializers.IntegerField(
        validators=[validate_stock_quantity],
        error_messages={
            'required': 'Stock quantity is required.',
            'invalid': 'Stock must be a valid integer.',
        }
    )
    
    description = serializers.CharField(
        min_length=10,
        error_messages={
            'required': 'Description is required.',
            'min_length': 'Description must be at least 10 characters.',
        }
    )
    
    class Meta:
        model = Product
        fields = "__all__"

