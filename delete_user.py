
import os
import django
import sys

# Add the project directory to the sys.path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

user_id = 17  # The ID from the error message

try:
    user = User.objects.get(id=user_id)
    print(f"Found user: {user.email} (ID: {user.id})")
    print("Deleting user and cascading to related objects...")
    user.delete()
    print("User and all related data deleted successfully.")
except User.DoesNotExist:
    print(f"User with ID {user_id} does not exist.")
except Exception as e:
    print(f"Error: {e}")
