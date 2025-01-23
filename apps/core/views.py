from django.shortcuts import render, redirect
from . import models
from . import forms
from django.contrib import messages 

def index(request):
    if 'workerID' in request.session:
        context = {
            'workerID': request.session['workerID'],
            'worker_first_name': request.session.get('worker_first_name', ''),
            'worker_last_name': request.session.get('worker_last_name', ''),
            'worker_permisson': request.session.get('worker_permission', ''),
        }
        return render(request, 'core/index.html', context)
    else:
        return redirect('workers:login')
