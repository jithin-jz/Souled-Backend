
import os
import django
import sys

# Add the project directory to the sys.path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
django.setup()

from orders.models import Order
from orders.serializers import OrderSerializer
import traceback

try:
    print("Fetching last 5 orders...")
    orders = Order.objects.all().order_by('-created_at')[:5]
    print(f"Found {len(orders)} orders.")
    
    for order in orders:
        print(f"--- Serializing Order {order.id} ---")
        try:
            serializer = OrderSerializer(order)
            data = serializer.data
            print("Success!")
            # print(data) # Uncomment if needed, but might be verbose
        except Exception as e:
            print(f"FAILED to serialize Order {order.id}")
            traceback.print_exc()
            break # Stop at first error
            
except Exception as e:
    print("General Error:")
    traceback.print_exc()
