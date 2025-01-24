from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Shift(models.Model):
    id = models.AutoField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    permission = models.IntegerField()
    sector = models.IntegerField()
    wage = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Worker(models.Model):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=150)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=150, unique=True)
    phone = PhoneNumberField(max_length=15, unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    hiring_date = models.DateField()
    firing_date = models.DateField(null=True, blank=True)
    raise_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name