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
            'worker_role': request.session.get('worker_role', ''),
        }
        return render(request, context, 'core/index.html')
    else:
        return redirect('workers:login')

def category(request):
    if 'workerID' in request.session:
        context = {
            'workerID': request.session['workerID'],
            'worker_first_name': request.session.get('worker_first_name', ''),
            'worker_last_name': request.session.get('worker_last_name', ''),
            'worker_permisson': request.session.get('worker_permission', ''),
            'worker_role': request.session.get('worker_role', ''),
        }

        form = forms.CategoryRegister()
        form_path = 'partials/forms/core/category.html'

        if request.method == 'POST':
            form = forms.CategoryRegister(request.POST)

            if form.is_valid():
                name = form.cleaned_data.get('name')
                type = form.cleaned_data.get('type')

                category = models.Category(
                    name = name,
                    type = type,
                )

                try:
                    category.save()
                    messages.success(request, "Categoria registrada com sucesso!")
                    return redirect('worker:index') 
                except Exception as e:
                    messages.error(request, f"Erro ao fazer o registro: {e}")

        return render(request,'partials/forms/template.html', {**context , 'form': form, 'form_path' : form_path})
    else:
        return redirect('workers:login')


def supplier(request):
    if 'workerID' in request.session:
        context = {
            'workerID': request.session['workerID'],
            'worker_first_name': request.session.get('worker_first_name', ''),
            'worker_last_name': request.session.get('worker_last_name', ''),
            'worker_permisson': request.session.get('worker_permission', ''),
            'worker_role': request.session.get('worker_role', ''),
        }

        form = forms.SupplierRegister()
        form_path = 'partials/forms/core/supplier.html'

        if request.method == 'POST':
            form = forms.SupplierRegister(request.POST)

            if form.is_valid():
                name = form.cleaned_data.get('name')
                quantity = form.cleaned_data.get('quantity')
                measurement = form.cleaned_data.get('measurement')
                image = form.cleaned_data.get('image')

                supplier = models.Supplier(
                    name = name,
                    quantity = quantity,
                    measurement = measurement,
                    image = image,
                )

                try:
                    supplier.save()
                    messages.success(request, "Produto registrado com sucesso!")
                    return redirect('worker:index') 
                except Exception as e:
                    messages.error(request, f"Erro ao fazer o registro: {e}")

        return render(request, 'partials/forms/template.html', {**context, 'form': form, 'form_path' : form_path})
    else:
        return redirect('workers:login')


def product(request):
    if 'workerID' in request.session:
        context = {
            'workerID': request.session['workerID'],
            'worker_first_name': request.session.get('worker_first_name', ''),
            'worker_last_name': request.session.get('worker_last_name', ''),
            'worker_permisson': request.session.get('worker_permission', ''),
            'worker_role': request.session.get('worker_role', ''),
        }
        form = forms.ProductRegister()
        form_path = 'partials/forms/core/product.html'

        if request.method == 'POST':
            form = forms.ProductRegister(request.POST, request.FILES)

            if form.is_valid():
                name = form.cleaned_data.get('name')
                quantity = form.cleaned_data.get('quantity')
                measurement = form.cleaned_data.get('measurement')
                individual_price = form.cleaned_data.get('individual_price')
                category = form.cleaned_data.get('category')
                image = form.cleaned_data.get('image')

                product = models.Product(
                    name = name,
                    quantity = quantity,
                    measurement = measurement,
                    individual_price = individual_price,
                    category = category,
                    image = image,
                )

                try:
                    product.save()
                    messages.success(request, "Fornecedor registrado com sucesso!")
                    return redirect('worker:index') 
                except Exception as e:
                    messages.error(request, f"Erro ao fazer o registro: {e}")

        return render(request, 'partials/forms/template.html', {**context, 'form': form, 'form_path' : form_path})
    else:
        return redirect('workers:login')

    
def meal(request):
    if 'workerID' in request.session:
        context = {
            'workerID': request.session['workerID'],
            'worker_first_name': request.session.get('worker_first_name', ''),
            'worker_last_name': request.session.get('worker_last_name', ''),
            'worker_permisson': request.session.get('worker_permission', ''),
            'worker_role': request.session.get('worker_role', ''),
        }

        form = forms.MealRegister()
        form_path = 'partials/forms/core/meal.html'

        if request.method == 'POST':
            form = forms.MealRegister(request.POST, request.FILES)

            if form.is_valid():
                name = form.cleaned_data.get('name')
                price = form.cleaned_data.get('price')
                category = form.cleaned_data.get('category')
                description = form.cleaned_data.get('description')
                calories = form.cleaned_data.get('calories')
                image = form.cleaned_data.get('image')

                meal = models.Meal(
                    name = name,
                    price = price,
                    category = category,
                    description = description,
                    calories = calories,
                    image = image,
                )

                try:
                    meal.save()
                    messages.success(request, "Refeição registrado com sucesso!")
                    return redirect('worker:index') 
                except Exception as e:
                    messages.error(request, f"Erro ao fazer o registro: {e}")

        return render(request, 'partials/forms/template.html', {**context, 'form': form, 'form_path' : form_path})
    else:
        return redirect('workers:login')
