from django.db import models

# Create your models here.
class UserModel(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=100)
    email=models.EmailField()
    acc_number=models.IntegerField()
    address=models.CharField(max_length=500)

    def __str__(self):
        return self.username
    
class Account(models.Model):
    user=models.ForeignKey(UserModel,on_delete=models.CASCADE)
    balance=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.user.username
    
class Transaction(models.Model):
    sender_name=models.CharField(max_length=100)
    receiver=models.ForeignKey(UserModel,on_delete=models.CASCADE)
    amount=models.PositiveBigIntegerField(default=0)
    def __str__(self):
        return self.sender_name

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    image=models.ImageField(upload_to='uploads/ingredient/',default=0)
    cost=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Product(models.Model):
    mealid=models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=100)
    image=models.ImageField(upload_to='uploads/product/',default=0)

    def __str__(self):
        return self.name

class ProductIngredient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=20)
    

    def __str__(self):
        return f"{self.product.name} - {self.ingredient.name}: {self.quantity}"