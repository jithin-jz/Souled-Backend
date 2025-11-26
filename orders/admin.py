from django.contrib import admin
from .models import Address, Order, OrderItem


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "city", "pincode", "phone")
    search_fields = ("full_name", "city", "pincode", "user__email")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "payment_status", "order_status", "payment_method", "total_amount", "created_at")
    list_filter = ("payment_status", "order_status", "payment_method", "created_at")
    search_fields = ("id", "user__email", "user__username")
    inlines = [OrderItemInline]
    readonly_fields = ("total_amount", "stripe_session_id", "created_at")
    ordering = ("-created_at",)

    # Disable add and delete for safety
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price")
    readonly_fields = ("order", "product", "quantity", "price")

    # Do not allow add or delete here either
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
