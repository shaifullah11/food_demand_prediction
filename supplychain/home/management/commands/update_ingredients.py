from django.core.management.base import BaseCommand
import csv
from home.models import Ingredient

class Command(BaseCommand):
    help = 'Update ingredients from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                cost = row['cost']
                name = row['name']
                default_image_path = f"C:\\Users\\shaif\\Desktop\\food_demand_prediction\\supplychain\\media\\uploads\\ingredient\\{name}.jpg"
                image_path = row.get('image', default_image_path)

                # Check if the ingredient with the given name already exists
                # If it exists, update its cost and image
                # If it doesn't exist, create a new Ingredient instance
                ingredient, created = Ingredient.objects.get_or_create(name=name)
                ingredient.cost = cost
                ingredient.image = image_path
                ingredient.save()

                # Additional fields can also be updated here if needed
                # ingredient.category = category
                # ingredient.cuisine = cuisine
                # ingredient.link = link
# python manage.py update_ingredients C:\Users\shaif\Desktop\food_demand_prediction\supplychain\recipes.csv