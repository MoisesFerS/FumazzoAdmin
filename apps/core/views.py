from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
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
        return render(request, 'core/index.html', context)
    else:
        return redirect('workers:login')
    
def stock(request):
    if 'workerID' in request.session:

        formAdd = forms.RestockRegister()
        formAdd_path = 'partials/forms/core/stock-add.html'

        formEdit = forms.RestockEdit()
        formEdit_path = 'partials/forms/core/stock-edit.html'

        restocks = models.Restock.objects.all().order_by('date')
        suppliers = models.Supplier.objects.all()
        receivers = models.Worker.objects.all()
        categories = models.Category.objects.filter(type=5)
        products = models.Product.objects.all()

        context = {
            'workerID': request.session['workerID'],
            'worker_first_name': request.session.get('worker_first_name', ''),
            'worker_last_name': request.session.get('worker_last_name', ''),
            'worker_permisson': request.session.get('worker_permission', ''),
            'worker_role': request.session.get('worker_role', ''),
            'restocks': restocks,
            'suppliers': suppliers,
            'receivers' : receivers,
            'categories' : categories,
            'products' : products,
            'formAdd' : formAdd,
            'formAdd_path' : formAdd_path,
            'formEdit' : formEdit,
            'formEdit_path' : formEdit_path,
        }

        return render(request, 'core/stock.html', context)
    else:
        return redirect('workers:login')

def restock_remove(request, id):
    if request.method == 'POST':
        if 'workerID' in request.session:
            if request.session.get('worker_permission', 0) >= 4:
                restock = get_object_or_404(models.Restock, id=id)
                restock.delete()
                
                return JsonResponse({'status': 'success', 'message': 'Registro deletado com sucesso!'})

            return JsonResponse({'status': 'error', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)

        return JsonResponse({'status': 'error', 'message': 'Usuário não autenticado.'}, status=403)

    return JsonResponse({'status': 'error', 'message': 'Método inválido.'}, status=405)


def restock_add(request):
    if request.method == 'POST':
        if 'workerID' in request.session:
            if request.session.get('worker_permission', 0) >= 4:
                date_ = request.POST.get('date')
                supplier_ = request.POST.get('supplier')
                receiver_ = request.POST.get('receiver')
                total_price_ = request.POST.get('total_price')

                supplier_ = get_object_or_404(models.Supplier, id=supplier_)
                receiver_ = get_object_or_404(models.Worker, id=receiver_)

                models.Restock.objects.create(
                    date=date_,
                    supplier=supplier_,
                    receiver=receiver_,
                    total_price=total_price_,
                )

                restocks = models.Restock.objects.all().order_by('date')

                return JsonResponse({
                    'status': 'success',
                    'message': 'Registro adicionado com sucesso!',       
                })
            
            else:
                return JsonResponse({'status': 'error', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)
        else:
            return JsonResponse({'status': 'error', 'message': 'Usuário não autenticado.'}, status=403)
    return JsonResponse({'status': 'error', 'message': 'Método inválido.'}, status=405)

def category(request):
    if 'workerID' in request.session:

        form = forms.CategoryRegister()
        form_path = 'partials/forms/core/category.html'

        if request.method == 'POST':
            form = forms.CategoryRegister(request.POST)

            if form.is_valid():
                name_ = form.cleaned_data.get('name')
                type_ = form.cleaned_data.get('type')

                category = models.Category(
                    name = name_,
                    type = type_,
                )

                try:
                    category.save()
                    messages.success(request, "Categoria registrada com sucesso!")
                    return redirect('worker:index') 
                except Exception as e:
                    messages.error(request, f"Erro ao fazer o registro: {e}")

        context = {
            'workerID': request.session['workerID'],
            'worker_first_name': request.session.get('worker_first_name', ''),
            'worker_last_name': request.session.get('worker_last_name', ''),
            'worker_permisson': request.session.get('worker_permission', ''),
            'worker_role': request.session.get('worker_role', ''),
            'form': form,
            'form_path' : form_path,
        }

        return render(request,'partials/forms/template.html', context)
    else:
        return redirect('workers:login')

def supplier(request):
    if 'workerID' in request.session:

        form = forms.SupplierRegister()
        form_path = 'partials/forms/core/supplier.html'

        if request.method == 'POST':
            form = forms.SupplierRegister(request.POST)

            if form.is_valid():
                name_ = form.cleaned_data.get('name')
                quantity_ = form.cleaned_data.get('quantity')
                measurement_ = form.cleaned_data.get('measurement')
                image_ = form.cleaned_data.get('image')

                supplier = models.Supplier(
                    name = name_,
                    quantity = quantity_,
                    measurement = measurement_,
                    image = image_,
                )

                try:
                    supplier.save()
                    messages.success(request, "Produto registrado com sucesso!")
                    return redirect('worker:index') 
                except Exception as e:
                    messages.error(request, f"Erro ao fazer o registro: {e}")

        context = {
            'workerID': request.session['workerID'],
            'worker_first_name': request.session.get('worker_first_name', ''),
            'worker_last_name': request.session.get('worker_last_name', ''),
            'worker_permisson': request.session.get('worker_permission', ''),
            'worker_role': request.session.get('worker_role', ''),
            'form': form, 
            'form_path' : form_path
        }

        return render(request, 'partials/forms/template.html', context)
    else:
        return redirect('workers:login')

def product(request):
    if 'workerID' in request.session:

        form = forms.ProductRegister()
        form_path = 'partials/forms/core/product.html'

        if request.method == 'POST':
            form = forms.ProductRegister(request.POST, request.FILES)

            if form.is_valid():
                name_ = form.cleaned_data.get('name')
                quantity_ = form.cleaned_data.get('quantity')
                measurement_ = form.cleaned_data.get('measurement')
                individual_price_ = form.cleaned_data.get('individual_price')
                category_ = form.cleaned_data.get('category')
                image_ = form.cleaned_data.get('image')

                product = models.Product(
                    name = name_,
                    quantity = quantity_,
                    measurement = measurement_,
                    individual_price = individual_price_,
                    category = category_,
                    image = image_,
                )

                try:
                    product.save()
                    messages.success(request, "Fornecedor registrado com sucesso!")
                    return redirect('worker:index') 
                except Exception as e:
                    messages.error(request, f"Erro ao fazer o registro: {e}")

        context = {
            'workerID': request.session['workerID'],
            'worker_first_name': request.session.get('worker_first_name', ''),
            'worker_last_name': request.session.get('worker_last_name', ''),
            'worker_permisson': request.session.get('worker_permission', ''),
            'worker_role': request.session.get('worker_role', ''),
            'form': form, 
            'form_path' : form_path
        }

        return render(request, 'partials/forms/template.html', context)
    else:
        return redirect('workers:login')
 
def meal(request):
    if 'workerID' in request.session:

        form = forms.MealRegister()
        form_path = 'partials/forms/core/meal.html'

        if request.method == 'POST':
            form = forms.MealRegister(request.POST, request.FILES)


            if form.is_valid():
                name_ = form.cleaned_data.get('name')
                price_ = form.cleaned_data.get('price')
                category_ = form.cleaned_data.get('category')
                description_ = form.cleaned_data.get('description')
                calories_ = form.cleaned_data.get('calories')
                image_ = form.cleaned_data.get('image')

                meal = models.Meal(
                    name = name_,
                    price = price_,
                    category = category_,
                    description = description_,
                    calories = calories_,
                    image = image_,
                )

                try:
                    meal.save()
                    messages.success(request, "Refeição registrado com sucesso!")
                    return redirect('worker:index') 
                except Exception as e:
                    messages.error(request, f"Erro ao fazer o registro: {e}")

        context = {
            'workerID': request.session['workerID'],
            'worker_first_name': request.session.get('worker_first_name', ''),
            'worker_last_name': request.session.get('worker_last_name', ''),
            'worker_permisson': request.session.get('worker_permission', ''),
            'worker_role': request.session.get('worker_role', ''),
            'form': form,
            'form_path' : form_path,
        }


        return render(request, 'partials/forms/template.html', context)
    else:
        return redirect('workers:login')
