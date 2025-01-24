from django.shortcuts import render, redirect
from . import models
from . import forms
from django.contrib import messages 
from .utils import bcrypt

def index(request):
    if 'workerID' in request.session:
        context = {
            'workerID': request.session['workerID'],
            'worker_first_name': request.session.get('worker_first_name', ''),
            'worker_last_name': request.session.get('worker_last_name', ''),
            'worker_permisson': request.session.get('worker_permission', ''),
            'worker_role': request.session.get('worker_role', ''),
        }
        
        return render(request, 'workers/index.html', context)
    else:
        return redirect('workers:login')

def login(request):
    form = forms.WorkerLogin()
    form_path = 'partials/forms/workers/login.html'

    if request.method == 'POST':
        form = forms.WorkerLogin(request.POST)  
        if form.is_valid(): 
            id_ = form.cleaned_data.get('id')
            password = form.cleaned_data.get('password')

            try:

                worker = models.Worker.objects.get(id=id_)
                role = worker.role
                worker_permission = role.permission
                worker_role = role.name

                if bcrypt.checkpw(password.encode('UTF-8'), worker.password.encode('UTF-8')):
                    request.session['workerID'] = worker.id
                    request.session['worker_first_name'] = worker.first_name
                    request.session['worker_last_name'] = worker.last_name
                    request.session['worker_permission'] = worker_permission
                    request.session['worker_role'] = worker_role                    

                    return redirect('workers:index')  
                else:

                    messages.error(request, 'Senha inválida')
            except models.Worker.DoesNotExist:

                messages.error(request, 'Usuário inválido')
        else:

            messages.error(request, 'Por favor, corrija os erros no formulário.')


    return render(request, 'workers/login.html', {'form': form, 'form_path': form_path})

def logout(request):
    request.session.flush()
    return redirect('workers:login')