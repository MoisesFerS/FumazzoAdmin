from django.shortcuts import render, redirect
from . import models
from . import forms
from django.contrib import messages 
from .utils import bcrypt

def index(request):

    if 'worker' in request.session:

        worker = models.Worker.objects.get(id = request.session['worker']['id'])
        role = worker.role
        sector = role.sector
        
        workerData = {
            'sector_id' : sector.id,
            'sector_name' : sector.name,
            'description' : role.description,
            'image': role.image.url if role.image else None
        }

        notifications = models.Notification.objects.filter(sector_id = workerData['sector_id'])

        context = {
            'worker': request.session.get('worker'),
            'workerRole': request.session.get('workerRole'),
            'workerData' : workerData,
            'notifications' : notifications,
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

                worker = models.Worker.objects.get(id = id_)

                if bcrypt.checkpw(password.encode('UTF-8'), worker.password.encode('UTF-8')):

                    role = worker.role                    

                    request.session['worker'] = {
                        'id' : worker.id,
                        'first_name' : worker.first_name,
                        'last_name' : worker.last_name,
                    }
                    request.session['workerRole'] = {
                        'permission' : role.permission,
                        'name': role.name,
                    }

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