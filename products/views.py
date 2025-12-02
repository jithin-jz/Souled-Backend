from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, AllowAny
from django.db.models import Q
from .models import Product
from .serializers import ProductSerializer


class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by("-created_at")
    filter_backends = [SearchFilter]
    search_fields = ["name", "description"]

    def get_queryset(self):
        queryset = super().get_queryset()

        category = self.request.query_params.get("category")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")

        if category:
            queryset = queryset.filter(category=category.lower())

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset


class ProductCreateView(CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]  # Only staff can create products


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    
    def get_permissions(self):
        # Allow anyone to view (GET), but only staff can update/delete
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]
