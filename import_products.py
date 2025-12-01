
import os
import json
import requests
import django
import sys
from django.core.files.base import ContentFile

# Add the project directory to the sys.path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
django.setup()

from products.models import Product

def import_products():
    json_file_path = 'products.json'
    
    if not os.path.exists(json_file_path):
        print(f"Error: {json_file_path} not found.")
        return

    with open(json_file_path, 'r') as f:
        data = json.load(f)

    products = data.get('products', [])
    print(f"Found {len(products)} products to import.")

    for item in products:
        name = item['name']
        
        # Check if product already exists to avoid duplicates
        if Product.objects.filter(name=name).exists():
            print(f"Skipping '{name}': Already exists.")
            continue

        print(f"Importing '{name}'...")
        
        # Download image
        image_url = item['image']
        image_content = None
        image_name = f"{name.replace(' ', '_').lower()}.jpg" # Default name

        try:
            if image_url:
                response = requests.get(image_url)
                response.raise_for_status()
                # Try to get filename from URL, else use generated name
                original_name = image_url.split('/')[-1].split('?')[0]
                if original_name:
                    image_name = original_name
                
                image_content = ContentFile(response.content)
        except Exception as e:
            print(f"  Warning: Failed to download image for '{name}': {e}")

        # Create product instance
        try:
            product = Product(
                name=name,
                price=item['price'],
                category=item['category'].lower(), # Convert to lowercase for model consistency
                description=item['description'],
                stock=item['stock']
            )
            
            if image_content:
                # save=False prevents saving the model immediately, we save it explicitly next
                product.image.save(image_name, image_content, save=False)
            
            product.save()
            print(f"  Successfully saved '{name}'.")
            
        except Exception as e:
            print(f"  Error saving product '{name}': {e}")

    print("\nImport process completed.")

if __name__ == "__main__":
    import_products()
