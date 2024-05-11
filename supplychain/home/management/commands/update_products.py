from django.core.management.base import BaseCommand
import csv
from home.models import Product

class Command(BaseCommand):
    help = 'Update products from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # Assuming your CSV columns are named 'meal_id', 'category', 'cuisine', and 'links'
                meal_id = int(row['meal_id'])
                category = row['category']
                cuisine = row['cuisine']
                link = row['links']

                # Check if the product with the given meal_id already exists
                # If it exists, update its category, cuisine, and links
                # If it doesn't exist, create a new Product instance
                product, created = Product.objects.get_or_create(mealid=meal_id)
                product.name = category  # Assuming category is the name of the product
                product.image = f"uploads/product/{category}.jpg"  # Assuming image names are based on category
                product.save()

                # Additional fields can also be updated here if needed
                # product.cuisine = cuisine
                # product.link = link



# python manage.py update_products C:\Users\shaif\Desktop\supplychain\supplychain\meal_info.csv
