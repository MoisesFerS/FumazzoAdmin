from django.db import models
from apps.workers.models import Worker
from phonenumber_field.modelfields import PhoneNumberField

class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    phone = PhoneNumberField(max_length=15)
    email = models.EmailField(max_length=150)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    type_choices = [
        (1, 'Lanches'),
        (2, 'Sobremesa Quente'),
        (3, 'Sobremesa Gelada'),
        (4, 'Bebida Quente'),
        (5, 'Bebida Gelada'),
        (6, 'Refrigerante'),
        (7, 'Suco'),
        (8, 'Alcólico'),
    ]
    type = models.IntegerField(choices=type_choices, default=1)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    individual_price = models.IntegerField()
    image = models.ImageField(upload_to='images/Products')
    status_choices = [
        (1, 'Cheio(100%)'),
        (2, 'Metade(50%)'),
        (3, 'Acabando(25%)'),
        (4, 'Vazio(0%)'),
    ]
    status = models.IntegerField(choices=status_choices, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    measurement_choices = [
        (1, 'Kilogramas'),
        (2, 'Gramas'),
        (3, 'Litros'),
        (4, 'Mililitros'),
        (5, 'Unidade'),
        (6, 'Pacote'),
    ]
    measurement = models.IntegerField(choices=measurement_choices, default=1)

class Restock(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Worker, on_delete=models.CASCADE)

class Resuply(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    restock = models.ForeignKey(Restock, on_delete=models.CASCADE)
    batch_price = models.DecimalField(max_digits=6, decimal_places=2)
    expiration_date = models.DateField()

class Meal(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    calories = models.IntegerField()
    image = models.ImageField(null=True, blank=True)

class Product_meal(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

class Category_meal(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)