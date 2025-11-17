from rest_framework import serializers
from .models import Address, Order, OrderItem


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "full_name", "phone", "street", "city", "pincode", "user"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        user = self.context["request"].user
        return Address.objects.create(user=user, **validated_data)


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    image = serializers.CharField(source="product.image", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "image", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "address",
            "items",
            "total_amount",
            "payment_method",
            "status",
            "stripe_session_id",
            "created_at",
        ]
        read_only_fields = [
            "user",
            "address",
            "items",
            "status",
            "stripe_session_id",
            "created_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        return Order.objects.create(user=user, **validated_data)
