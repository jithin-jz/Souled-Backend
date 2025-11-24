from django.urls import path
from .views import (
    CreateOrderAPIView,
    StripeWebhookAPIView,
    VerifyPaymentAPIView,
    UserOrderListAPIView,
)
from .address_views import (
    UserAddressListCreateView,
    UserAddressDetailView,
)

urlpatterns = [
    path("create/", CreateOrderAPIView.as_view(), name="order-create"),
    path("webhook/", StripeWebhookAPIView.as_view(), name="stripe-webhook"),
    path("verify-payment/", VerifyPaymentAPIView.as_view(), name="verify-payment"),
    path("my/", UserOrderListAPIView.as_view(), name="user-orders"),
    
    # Address management
    path("addresses/", UserAddressListCreateView.as_view(), name="address-list-create"),
    path("addresses/<int:address_id>/", UserAddressDetailView.as_view(), name="address-detail"),
]