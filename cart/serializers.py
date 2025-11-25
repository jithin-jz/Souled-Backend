from rest_framework import serializers
from .models import Cart, CartItem, Wishlist, WishlistItem
from products.serializers import ProductSerializer
from utils import validate_quantity_range


# CART
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(
        error_messages={
            'required': 'Product ID is required.',
            'invalid': 'Product ID must be a valid integer.',
        }
    )
    quantity = serializers.IntegerField(
        default=1,
        validators=[validate_quantity_range],
        error_messages={
            'required': 'Quantity is required.',
            'invalid': 'Quantity must be a valid integer.',
        }
    )


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "items"]


# WISHLIST
class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = WishlistItem
        fields = ["id", "product"]


class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = ["id", "items"]


class AddToWishlistSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
