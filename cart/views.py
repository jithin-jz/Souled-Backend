from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Cart, CartItem, Wishlist, WishlistItem
from .serializers import (
    CartSerializer, AddToCartSerializer,
    WishlistSerializer, AddToWishlistSerializer
)
from products.models import Product


# Helpers
def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

def get_user_wishlist(user):
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    return wishlist


# ============================
# CART
# ============================
class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_user_cart(request.user)
        return Response(CartSerializer(cart).data)


class AddToCartView(APIView):
    """
    Add product to cart.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = get_user_cart(request.user)
        product = get_object_or_404(Product, id=serializer.validated_data["product_id"])
        quantity = serializer.validated_data["quantity"]

        # Check stock availability
        if product.stock < quantity:
            return Response(
                {"error": f"Only {product.stock} item(s) available in stock."},
                status=400
            )
        
        # Check if adding to existing cart item would exceed stock
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            new_quantity = item.quantity + quantity
            if product.stock < new_quantity:
                return Response(
                    {"error": f"Cannot add {quantity} more. Only {product.stock - item.quantity} item(s) available."},
                    status=400
                )
            item.quantity = new_quantity
        else:
            item.quantity = quantity

        item.save()
        return Response({"message": "Added to cart"})


class RemoveFromCartView(APIView):
    """
    Remove cart item.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        cart = get_user_cart(request.user)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        return Response({"message": "Removed"})


class UpdateCartQuantityView(APIView):
    """
    Update cart item quantity.
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        quantity = request.data.get("quantity")
        if not quantity or quantity < 1:
            return Response({"error": "Invalid quantity"}, status=400)
        
        if quantity > 99:
            return Response({"error": "Maximum quantity per item is 99"}, status=400)

        cart = get_user_cart(request.user)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        # Check stock availability
        if item.product.stock < quantity:
            return Response(
                {"error": f"Only {item.product.stock} item(s) available in stock."},
                status=400
            )
        
        item.quantity = quantity
        item.save()

        return Response({"message": "Quantity updated"})


class ClearCartView(APIView):
    """
    Clear all items from cart.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cart = get_user_cart(request.user)
        CartItem.objects.filter(cart=cart).delete()
        return Response({"message": "Cart cleared successfully"})


# ============================
# WISHLIST
# ============================
class WishlistDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist = get_user_wishlist(request.user)
        return Response(WishlistSerializer(wishlist).data)


class AddToWishlistView(APIView):
    """
    Add to wishlist.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddToWishlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wishlist = get_user_wishlist(request.user)
        product = get_object_or_404(Product, id=serializer.validated_data["product_id"])

        item, created = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)

        if not created:
            return Response({"message": "Already in wishlist"})

        return Response({"message": "Added to wishlist"})


class RemoveFromWishlistView(APIView):
    """
    Remove from wishlist.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        wishlist = get_user_wishlist(request.user)
        item = get_object_or_404(WishlistItem, id=item_id, wishlist=wishlist)
        item.delete()
        return Response({"message": "Removed from wishlist"})
