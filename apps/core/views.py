from django.shortcuts import render, redirect
from . import models
from . import forms
from django.contrib import messages 
from .utils import bcrypt

def index(request):
    if 'workerID' in request.session:
        return render(request, 'core/index.html')
    
    else:
        return redirect('login')

def login(request):
    form = forms.WorkerLogin()

    if request.method == 'POST':
        form = forms.WorkerLogin(request.POST)  
        if form.is_valid(): 
            id = form.cleaned_data.get('id')
            password = form.cleaned_data.get('password')

        try:

            worker = models.Worker.objects.get(id=id)

            if bcrypt.checkpw(password.encode('UTF-8'), worker.password.encode('UTF-8')):
                request.session['workerID'] = worker.id
                request.session['worker_first_name'] = worker.first_name
                request.session['worker_last_name'] = worker.last_name
                return redirect('index')  
            else:
                messages.error(request, 'Senha inválida')
        except models.Worker.DoesNotExist:
            messages.error(request, 'Usuário inválido')

        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')

    return render(request, 'core/login.html', {'form': form})
