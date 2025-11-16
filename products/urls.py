from django.urls import path
from .views import ProductListCreateAPIView, ProductDetailAPIView

urlpatterns = [
    path('', ProductListCreateAPIView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
]
