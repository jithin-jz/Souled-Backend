from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from panel.serializers import UserSerializer

User = get_user_model()


class AdminUserList(ListAPIView):
    queryset = User.objects.all().order_by("-id")
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class AdminUserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
    permission_classes = [IsAdminUser]


class AdminToggleBlockUser(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        user.is_block = not user.is_block
        user.save()

        return Response({"status": "success", "isBlock": user.is_block}, status=200)


class AdminDeleteUser(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        user.delete()
        return Response({"status": "deleted"}, status=200)


class DashboardStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        from products.models import Product
        from orders.models import Order
        from django.db.models import Sum

        total_users = User.objects.count()
        total_products = Product.objects.count()
        total_orders = Order.objects.count()
        
        # Calculate total revenue from paid orders
        revenue_data = Order.objects.filter(payment_status="paid").aggregate(
            total_revenue=Sum("total_amount")
        )
        total_revenue = revenue_data["total_revenue"] or 0

        # Get recent orders
        recent_orders = Order.objects.all().order_by("-created_at")[:5]
        from orders.serializers import OrderSerializer
        recent_orders_data = OrderSerializer(recent_orders, many=True).data

        # Get category distribution
        category_data = []
        categories = Product.objects.values_list('category', flat=True).distinct()
        for cat in categories:
            count = Product.objects.filter(category=cat).count()
            category_data.append({"name": cat, "count": count})

        # Get top products by stock (or sales if available, but stock for now)
        # Actually, let's show low stock products as it's more useful for admin
        low_stock_products = Product.objects.order_by("stock")[:5]
        from products.serializers import ProductSerializer
        low_stock_data = ProductSerializer(low_stock_products, many=True).data

        return Response({
            "total_users": total_users,
            "total_products": total_products,
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "recent_orders": recent_orders_data,
            "category_data": category_data,
            "low_stock_products": low_stock_data,
        })


class AdminReportsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        from orders.models import Order
        from django.db.models import Sum, Count
        from django.db.models.functions import TruncDate

        # Total Stats
        total_orders = Order.objects.count()
        revenue_data = Order.objects.filter(payment_status="paid").aggregate(
            total_revenue=Sum("total_amount")
        )
        total_revenue = revenue_data["total_revenue"] or 0

        # Revenue Timeline (Group by Date)
        timeline_data = (
            Order.objects.filter(payment_status="paid")
            .annotate(date=TruncDate("created_at"))
            .values("date")
            .annotate(total=Sum("total_amount"))
            .order_by("date")
        )
        
        revenue_timeline = [
            {"name": item["date"].strftime("%Y-%m-%d"), "total": item["total"]}
            for item in timeline_data
        ]

        # Payment Method Distribution
        payment_counts = (
            Order.objects.values("payment_method")
            .annotate(count=Count("id"))
            .order_by("payment_method")
        )
        payment_distribution = [
            {"name": item["payment_method"].upper(), "count": item["count"]}
            for item in payment_counts
        ]

        # Order Status Distribution
        status_counts = (
            Order.objects.values("order_status")
            .annotate(count=Count("id"))
            .order_by("order_status")
        )
        status_distribution = [
            {"name": item["order_status"].title(), "count": item["count"]}
            for item in status_counts
        ]

        return Response({
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "revenue_timeline": revenue_timeline,
            "payment_distribution": payment_distribution,
            "status_distribution": status_distribution,
        })
