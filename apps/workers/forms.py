from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Role, Shift

class ShiftRegister(forms.Form):
    name = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={'class': 'form-input-'})
    )

    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})
    )

    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})
    )

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("O horário de início deve ser anterior ao horário de término.")

class RoleRegister(forms.Form):
    name = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={'class': 'form-input-'})  
    )
        
    permission = forms.ChoiceField(
        choices=[
            (1, 'Funcionário'),
            (2, 'Líder de Equipe'),
            (3, 'Supervisor'),
            (4, 'Gerente'),
            (5, 'Diretor'),
            (6, 'CEO'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial=1
    )

    sector = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-input-'}) 
    )

    wage = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-input-', 'step': '0.01'}) 
    )

class WorkerRegister(forms.Form):
    first_name = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={'class': 'form-input-'})  
    )

    last_name = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={'class': 'form-input-'})  
    )

    email = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-input-'})  
    )

    phone = PhoneNumberField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input-'})
        )

    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        widget=forms.Select(attrs={'class': 'form-input-'})
    )

    shift = forms.ModelChoiceField(
        queryset=Shift.objects.all(),
        widget=forms.Select(attrs={'class': 'form-input-'})
    )

class WorkerLogin(forms.Form):
    id = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-input-id', 'placeholder' : 'ID'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input-password', 'placeholder' : 'SENHA'})
    )

