from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Supplier
from workers.models import Worker

class SupplierRegister(forms.Form):
    name = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={'class': ''})
    )

    address = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': ''})
    )

    phone = PhoneNumberField(
        required=False,
        widget=forms.TextInput(attrs={'class': ''})
    )

    email = forms.CharField(
        required=False,
        max_length=150, 
        widget=forms.TextInput(attrs={'class': ''})
    )

    def clean(self):
        cleaned_data = super().clean()

        phone = cleaned_data.get('phone')
        email = cleaned_data.get('email')

        if not phone and not email:
            raise forms.ValidationError("Insira alguma forma de contato.")
        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not name:
            raise forms.ValidationError('Insira o nome do fornecedor.')
        return name

    def clean_address(self):
        address = self.cleaned_data.get('address')

        if not address:
            raise forms.ValidationError('Insira o endereço do fornecedor.')
        return address

class ProductRegister(forms.Form):
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': ''}),
    )

    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': ''}),
        
    )

    measurement = forms.ChoiceField(
        choices=[
            (1, 'Kilogramas'),
            (2, 'Gramas'),
            (3, 'Litros'),
            (4, 'Mililitros'),
            (5, 'Unidade'),
            (6, 'Pacote'),
        ],
        widget=forms.RadioSelect(attrs={'class': ''}),
    )

    individual_price = forms.DecimalField(
        min_value=0.01,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': ''}),
    )

    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': ''}),
    )

    type = forms.ChoiceField(
        choices=[
            (1, 'Ingrediente'),
            (2, 'Limpeza'),
            (3, 'Higiene'),
            (4, 'Molho'),
            (5, 'Bebida'),
            (6, 'Sorvete'),
        ],
        widget=forms.RadioSelect(attrs={'class': ''}),
    )

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 0:
            raise forms.ValidationError('A quantidade deve ser positiva.')
        return quantity

    def clean_individual_price(self):
        individual_price = self.cleaned_data.get('individual_price')
        if individual_price is not None and individual_price < 0:
            raise forms.ValidationError('O preço deve ser positivo.')
        return individual_price

class CategoryRegister(forms.Form):
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': ''}),
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not name:
            raise forms.ValidationError('Insira o nome da categoria.')
        return name
    
class RestockRegister(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': '', 'type': 'date'}),
    )

    total_price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': ''}),
    )

    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.all(),
        widget=forms.Select(attrs={'class': ''}),
    )

    receiver = forms.ModelChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.Select(attrs={'class': ''}),
    )

class MealRegister(forms.Form):
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': ''}),
    )

    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': ''}),
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': ''})
    )

    calories = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': ''})
    )

    image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': ''})
    )
    
    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price < 0:
            raise forms.ValidationError('O valor deve ser positivo.')
        return price
    
    def clean_calories(self):
        calories = self.cleaned_data.get('calories')

        if calories < 0:
            raise forms.ValidationError('O valor deve ser positivo.')
        return calories
    