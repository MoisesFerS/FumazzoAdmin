from django.db import models
from apps.workers.models import Worker
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify 

class Unit(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='core/units/', null=True, blank=True)
    address = models.CharField(max_length=150)
    phone = PhoneNumberField()
    email = models.EmailField(max_length=150)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

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
        (1, 'Lanche'),
        (2, 'Sobremesa'),
        (3, 'Porção'),
        (4, 'Bebida'),
        (5, 'Produto'),
        (6, 'Ingrediente'),
        (7, 'Ticket'),
    ]
    type = models.IntegerField(choices=type_choices, default=1)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    sell_price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    image = models.ImageField(upload_to='core/products/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    measurement_choices = [
        (1, 'Kilogramas'),
        (2, 'Gramas'),
        (3, 'Litros'),
        (4, 'Mililitros'),
        (5, 'Unidade'),
        (6, 'Pacote'),
    ]
    measurement = models.IntegerField(choices=measurement_choices, default=1)

class Stock(models.Model):
    from apps.workers.models import Worker
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    total_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Worker, on_delete=models.CASCADE)

class Supply(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Meal(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='core/meals/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

class Ingredient(models.Model):
    ingredient = models.ForeignKey(Product, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'meal'], name='pk_ingredient_meal')
        ]

class Ticket(models.Model):
    from apps.workers.models import Sector
    id = models.AutoField(primary_key=True)
    reason = models.TextField()
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    priority = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.IntegerField(default=0)

class Table(models.Model):
    id = models.AutoField(primary_key=True)
    chairs = models.IntegerField()
    floor = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='core/tables/', null=True, blank=True)

class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    discount = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    type_choices = [
        (1, '%'),
        (2, 'R$:'),
    ]
    type = models.IntegerField(choices=type_choices, default=1)