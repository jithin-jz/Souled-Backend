
import os
import django
import sys

# Add the project directory to the sys.path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
django.setup()

from products.models import Product

try:
    count = Product.objects.count()
    print(f"Deleting {count} products...")
    Product.objects.all().delete()
    print("All products deleted successfully.")
except Exception as e:
    print(f"Error: {e}")
