from django.contrib import admin
from django.utils.html import format_html
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "stock", "image_tag", "created_at")
    list_filter = ("category",)
    search_fields = ("name", "description")
    ordering = ("-created_at",)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:80px; height:auto;" />', obj.image.url)
        return "-"
    image_tag.short_description = "Image"
