import csv
from django.core.management.base import BaseCommand
from home.models import Ingredient, Product, ProductIngredient

class Command(BaseCommand):
    help = 'Updates ProductIngredient instances with data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    product = Product.objects.get(name=row['category'])
                    ingredient = Ingredient.objects.get(name=row['ingredient'])
                    quantity = row['quantity'].strip()  # No need to convert to float
                    product_ingredient, created = ProductIngredient.objects.get_or_create(product=product, ingredient=ingredient)
                    product_ingredient.quantity = quantity
                    product_ingredient.save()
                except Product.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Product '{row['category']}' does not exist."))
                except Ingredient.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Ingredient '{row['ingredient']}' does not exist."))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
