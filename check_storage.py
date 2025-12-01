
import os
import django
import sys
from django.conf import settings

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
django.setup()

from django.core.files.storage import default_storage

print(f"Default Storage: {default_storage}")
print(f"Backend: {default_storage.__class__.__name__}")
