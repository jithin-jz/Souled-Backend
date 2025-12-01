
import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
django.setup()

from products.models import Product

count = Product.objects.count()
print(f"Total Products: {count}")

if count > 0:
    p = Product.objects.first()
    print(f"Sample Product: {p.name}")
    print(f"Image URL: {p.image.url if p.image else 'No Image'}")
