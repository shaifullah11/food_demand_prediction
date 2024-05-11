from django.core.management.base import BaseCommand
from home.models import Ingredient  # Import your Ingredient model

class Command(BaseCommand):
    help = 'Prints all Ingredients with their associated image names'

    def handle(self, *args, **kwargs):
        ingredients = Ingredient.objects.all()
        for ingredient in ingredients:
            self.stdout.write(f"{ingredient.name} - {ingredient.image.name}")
