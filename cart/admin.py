from django.contrib import admin
from .models import Cart, CartItem, Wishlist, WishlistItem


# ================
# Cart
# ================
class CartItemInline(admin.TabularInline):
    model = CartItem
    readonly_fields = ("product", "quantity")
    can_delete = False
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("user__username", "user__email")
    inlines = [CartItemInline]
    readonly_fields = ("user", "created_at")

    def has_add_permission(self, request):
        return False


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# ================
# Wishlist
# ================
class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    readonly_fields = ("product",)
    can_delete = False
    extra = 0


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("user__username", "user__email")
    inlines = [WishlistItemInline]
    readonly_fields = ("user", "created_at")

    def has_add_permission(self, request):
        return False


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ("wishlist", "product")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
