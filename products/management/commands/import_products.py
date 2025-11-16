import json
import requests
from django.core.management.base import BaseCommand
from products.models import Product
import cloudinary.uploader


class Command(BaseCommand):
    help = "Import products with direct byte-upload to Cloudinary"

    def handle(self, *args, **kwargs):
        with open("products.json", "r") as file:
            data = json.load(file)

        for item in data["products"]:

            print(f"Downloading {item['name']}")

            # Clean URL
            raw_url = item["image"]
            clean_url = raw_url.split("?")[0]

            # Download image BYTES
            try:
                response = requests.get(clean_url, timeout=10)
                response.raise_for_status()
                image_bytes = response.content
            except Exception:
                print(f"❌ Failed to download: {clean_url}")
                continue

            # Upload BYTES directly to Cloudinary
            try:
                upload_result = cloudinary.uploader.upload(image_bytes)
                cloud_url = upload_result["secure_url"]
            except Exception as e:
                print(f"❌ Cloudinary upload failed for {item['name']}: {e}")
                continue

            # Save Product
            Product.objects.create(
                name=item["name"],
                price=item["price"],
                category=item["category"],
                description=item["description"],
                stock=item["stock"],
                image=cloud_url,  # URLField
            )

            print(f"✅ Imported {item['name']}")
