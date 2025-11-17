from django.urls import path
from .views import (
    CreateOrderAPIView,
    StripeWebhookAPIView,
    VerifyPaymentAPIView,
)

urlpatterns = [
    path("create/", CreateOrderAPIView.as_view(), name="order-create"),
    path("webhook/", StripeWebhookAPIView.as_view(), name="stripe-webhook"),
    path("verify-payment/", VerifyPaymentAPIView.as_view(), name="verify-payment"),
]
