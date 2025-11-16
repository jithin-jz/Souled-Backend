from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("Men", "Men"),
        ("Women", "Women"),
    ]

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    image = models.URLField(max_length=500, null=True, blank=True)   # FIXED
    description = models.TextField()
    stock = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name