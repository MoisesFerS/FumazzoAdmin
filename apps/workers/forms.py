from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Role, Shift

class ShiftRegister(forms.Form):
    name = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={'class': 'input-primary'})
    )

    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'input-primary'})
    )

    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'input-primary'})
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
        widget=forms.TextInput(attrs={'class': 'input-primary'})  
    )
        
    permission = forms.ChoiceField(
        choices=[
            (1, 'Funcionário'), 
            (2, 'Líder de Equipe'), 
            (3, 'Supervisor'), 
            (4, 'Gerente'), 
            (5, 'Diretor'), 
            (6, 'CEO')],
        widget=forms.RadioSelect(attrs={'class': 'select-main-primary'}),
        initial=1
    )

    sector = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'input-primary'}) 
    )

    wage = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'input-primary'}) 
    )

class WorkerRegister(forms.Form):
    first_name = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={'class': 'input-primary'})  
    )

    last_name = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={'class': 'input-primary'})  
    )

    email = forms.CharField(
        max_length=150, 
        widget=forms.EmailInput(attrs={'class': 'input-primary'})  
    )

    phone = PhoneNumberField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input-primary'})
    )

    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        widget=forms.Select(attrs={'class': 'input-primary'})
    )

    shift = forms.ModelChoiceField(
        queryset=Shift.objects.all(),
        widget=forms.Select(attrs={'class': 'input-primary'})
    )

class WorkerLogin(forms.Form):
    id = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'input-primary', 'placeholder': 'ID'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input-primary', 'placeholder': 'SENHA'})
    )
