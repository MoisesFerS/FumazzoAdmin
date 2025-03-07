from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from . import models
from . import forms
from django.contrib import messages 
from django.db.models import Q
import json
from apps.workers.models import Worker, Sector

#   ============================================================
#   INDEX - Defs related to Index page(manage)
#   ============================================================ 

# Render index page
def index(request):

  if 'worker' not in request.session:
    return redirect('workers:login')
  
  context = {
    'worker': request.session.get('worker'),
    'workerRole': request.session.get('workerRole'),
  }
  return render(request, 'core/index.html', context)    

#   ============================================================
#   STOCK SYSTEM - Defs related to Stock page
#   ============================================================ 

# Render Stock page
def stock(request):

  if 'worker' not in request.session:
    return redirect('workers:login')

  stocks = models.Stock.objects.all().order_by('date')
  suppliers = models.Supplier.objects.all()
  receivers = Worker.objects.all()

  context = {
    'worker': request.session.get('worker'),
    'workerRole': request.session.get('workerRole'),
    'stocks': stocks,
    'suppliers': suppliers,
    'receivers' : receivers,
  }

  return render(request, 'core/stock.html', context)

# Gets the Products and Categories shown in the select 
def get_products(request):

  if request.session.get('workerRole', {}).get('permission', 0) < 4:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)
  
  categories = models.Category.objects.filter(Q(type=5) | Q(type=4))
  products = models.Product.objects.all()
  data = []
  for category in categories:
    products_in_category = [
      {'id': product.id, 'name': product.name}
      for product in products if product.category.id == category.id
    ]
    data.append({
      'categories': category.name,
      'products': products_in_category
    })
    
  return JsonResponse(data, safe=False)

# Add a stock entry
def stock_add(request):

  if request.method != 'POST':
    return JsonResponse({'status': 'error', 'error': '405', 'message': 'Método inválido.'}, status=405)

  if 'worker' not in request.session:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autenticado.'}, status=403)

  if request.session.get('workerRole', {}).get('permission', 0) < 4:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)
  
  try:
    data = json.loads(request.body)

    if not data.get('date'):
      return JsonResponse({'status': 'error', 'error': '400', 'message': 'Preencha todos os campos.'}, status=400)

    date_ = data.get('date')                    
    supplier_ = models.Supplier.objects.filter(id = data.get('supplier')).first()
    receiver_ =  models.Worker.objects.filter(id = data.get('receiver')).first()

    models.Stock.objects.create(
      date = date_,
      supplier = supplier_,
      receiver = receiver_,
    )

    return JsonResponse({'status': 'success', 'message': 'Registro alterado com sucesso!'})

  except json.JSONDecodeError:
    return JsonResponse({'status': 'error', 'error': '400', 'message': 'Erro ao processar JSON'}, status=400)

# Loads every Product from a Stock entry in the Edit Modal
def load_product(request, id):

  stock = get_object_or_404(models.Stock, id=id)
  resupplies = stock.supply_set.all()

  data = []
  
  for supply in resupplies:
    current_product = supply.product.id 
    data.append({
      'current_product': current_product, 
      'quantity': supply.quantity,
      'price': str(supply.price),
    })
  
  return JsonResponse({'status': 'success', 'message': 'Produtos carregados com sucesso', 'data' : data})

# Save a stock entry edit
def stock_edit_save(request, id):

  if request.method != 'POST':
    return JsonResponse({'status': 'error', 'error': '405', 'message': 'Método inválido.'}, status=405)

  if 'worker' not in request.session:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autenticado.'}, status=403)

  if request.session.get('workerRole', {}).get('permission', 0) < 4:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)

  try:
    data = json.loads(request.body)
    edit = data.get('edit', {})
    products = data.get('products', [])

    stock = get_object_or_404(models.Stock, id=id)
    supplies = models.Supply.objects.filter(stock_id=id)

    total_price_ = 0
    product_ids = []

    for product in products:
      item_ = product.get('item')
      quantity_ = int(product.get('quantity', 0))
      price_ = float(product.get('price', 0.0))

      if not item_:
        continue  

      supply = supplies.filter(product_id=item_).first()

      if supply:
        supply.quantity = quantity_
        supply.price = price_
        supply.save()
      else:
        supply = models.Supply.objects.create(
          stock_id=id,
          quantity=quantity_,
          product_id=item_,
          price=price_,
        )

      total_price_ += supply.price
      product_ids.append(item_)

    stock.date = edit.get('date')
    stock.receiver_id = edit.get('receiver')
    stock.supplier_id = edit.get('supplier')
    stock.total_price = total_price_
    stock.save()

    supplies.exclude(product_id__in=product_ids).delete()

    return JsonResponse({'status': 'success', 'message': 'Registro alterado com sucesso!'})

  except json.JSONDecodeError:
    return JsonResponse({'status': 'error', 'error': '400', 'message': 'Erro ao processar JSON'}, status=400)
  
# Removes a Stock entry
def stock_remove(request, id):

  if request.method != 'POST':
    return JsonResponse({'status': 'error', 'error': '405', 'message': 'Método inválido.'}, status=405)

  if 'worker' not in request.session:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autenticado.'}, status=403)

  if request.session.get('workerRole', {}).get('permission', 0) < 4:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)
  
  try:

    stock = get_object_or_404(models.Stock, id = id)
    stock.delete()

    return JsonResponse({'status': 'success', 'message': 'Registro alterado com sucesso!'})

  except json.JSONDecodeError:
    return JsonResponse({'status': 'error', 'error': '400', 'message': 'Erro ao processar JSON'}, status=400)

# Add a Ticket entry
def ticket_add(request):

  if request.method != 'POST':
    return JsonResponse({'status': 'error', 'error': '405', 'message': 'Método inválido.'}, status=405)

  if 'worker' not in request.session:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autenticado.'}, status=403)

  try:
    data = json.loads(request.body)

    if not data.get('reason'):
      return JsonResponse({'status': 'error', 'error': '400', 'message': 'Preencha todos os campos.'}, status=400)

    if not data.get('description'):
      return JsonResponse({'status': 'error', 'error': '400', 'message': 'Preencha todos os campos.'}, status=400)

    reason_ = data.get('reason')
    sector_ = Sector.objects.filter(id = data.get('sector')).first()
    priority_ = data.get('priority')
    category_ = models.Category.objects.filter(id = data.get('category')).first()
    description_ = data.get('description')

    models.Ticket.objects.create(
      reason = reason_,
      sector = sector_,
      priority = priority_,
      category = category_,
      description = description_,
    )

    return JsonResponse({'status': 'success', 'message': 'Registro alterado com sucesso!'})

  except json.JSONDecodeError:
    return JsonResponse({'status': 'error', 'error': '400', 'message': 'Erro ao processar JSON'}, status=400)

def meal(request):
  if 'worker' not in request.session:
    return redirect('workers:login')
  
  types = [1, 2, 3, 4] 
  entries = { 
    1: {"name": "LANCHES", "categories": []}, 
    2: {"name": "SOBREMESAS", "categories": []},
    3: {"name": "PORÇÕES", "categories": []},
    4: {"name": "BEBIDAS", "categories": []}
  }


  for type in types:
    categories = models.Category.objects.filter(type=type)

    for category in categories:
      category_data = {
        "category_name": category.name,  
        "category_id": category.id,
        "meals": []  
      }
        
      meals = models.Meal.objects.filter(category=category)
        
      for meal in meals:
        category_data["meals"].append({"meal_name": meal.name, "meal_id": meal.id})

      entries[type]["categories"].append(category_data)

  context = {
    'worker': request.session.get('worker'),
    'workerRole': request.session.get('workerRole'),
    'entries': entries,
  }

  return render(request, 'core/meal.html', context)


# ===== TESTS =====

def category(request):
    if 'worker' not in request.session:

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
            'workerRole.permission': request.session.get('workerRole.permission', ''),
            'worker_role': request.session.get('worker_role', ''),
            'form': form,
            'form_path' : form_path,
        }

        return render(request,'partials/forms/template.html', context)
    else:
        return redirect('workers:login')

def supplier(request):
    if 'worker' not in request.session:

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
            'workerRole.permission': request.session.get('workerRole.permission', ''),
            'worker_role': request.session.get('worker_role', ''),
            'form': form, 
            'form_path' : form_path
        }

        return render(request, 'partials/forms/template.html', context)
    else:
        return redirect('workers:login')

def product(request):
    if 'worker' not in request.session:

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
            'workerRole.permission': request.session.get('workerRole.permission', ''),
            'worker_role': request.session.get('worker_role', ''),
            'form': form, 
            'form_path' : form_path
        }

        return render(request, 'partials/forms/template.html', context)
    else:
        return redirect('workers:login')
 