from django.contrib import admin
from .models import UserModel,Account,Ingredient,ProductIngredient,Product
# Register your models here.

admin.site.register(UserModel)
admin.site.register(Ingredient)
admin.site.register(ProductIngredient)
admin.site.register(Product)
