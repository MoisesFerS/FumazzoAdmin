from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from . import models
from . import forms
from django.contrib import messages 
from django.db.models import Q
import json
from apps.workers.models import Worker, Sector
from django.core.files.base import ContentFile

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
  
  categories = models.Category.objects.filter(Q(type=4) | Q(type=5) | Q(type=6))
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
    receiver_ =  Worker.objects.filter(id = data.get('receiver')).first()

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

  types = [
    (1, 'LANCHES'),
    (2, 'SOBREMESAS'),
    (3, 'PORÇÕES'),
    (4, 'BEBIDAS')
  ]

  entries = {type_id: {"name": type_name, "categories": []} for type_id, type_name in types}

  for type_id, type_name in types:
    categories = models.Category.objects.filter(type=type_id)

    for category in categories:
      category_data = {
        "category_name": category.name,
        "category_id": category.id,
        "items": [] 
      }

      if type_id in [1, 2, 3]:
        meals = models.Meal.objects.filter(category=category)
        for meal in meals:
          meal_data = {
              "id": meal.id,
              "name": meal.name,
              "price": meal.price,
              "description": meal.description,
              "image": meal.image,
              "ingredient_set": []
          }

          ingredients = models.Ingredient.objects.filter(meal=meal)

          for ingredient in ingredients:
              meal_data["ingredient_set"].append({
                  "product": {
                      "id": ingredient.ingredient.id,
                      "name": ingredient.ingredient.name,
                      "image": ingredient.ingredient.image.url if ingredient.ingredient.image else None
                  },
                  "quantity": ingredient.quantity
              })

          category_data["items"].append(meal_data)

      elif type_id == 4:
        products = models.Product.objects.filter(category=category)
        for product in products:
          category_data["items"].append({
            "name": product.name,
            "price": product.sell_price,
            "quantity": product.quantity,
            "image": product.image
          })

      entries[type_id]["categories"].append(category_data)

  context = {
    'worker': request.session.get('worker'),
    'workerRole': request.session.get('workerRole'),
    'entries': entries,
  }

  return render(request, 'core/meal.html', context)

def get_categories(request, id):
  try:
    type_id = id

    categories = list(models.Category.objects.filter(type=type_id).values('id', 'name'))

    if categories:
      return JsonResponse({'status': 'success', 'message': 'Categorias carregadas com sucesso', 'data': categories})
    else:
      return JsonResponse({'status': 'success', 'message': 'Nenhuma categoria encontrada para este tipo'})

  except ValueError:
    return JsonResponse({'status': 'error', 'message': 'ID inválido'}, status=400)

def get_ingredients(request):
  try:
    categories = models.Category.objects.filter(type=6).values('id', 'name')
    ingredients_data = []

    for category in categories:

      products = models.Product.objects.filter(category_id=category['id']).values('id', 'name')
      ingredients_data.append({ 'category': category['name'], 'ingredients': list(products)})

    return JsonResponse({ 'status': 'success', 'message': 'Ingredientes carregados com sucesso', 'data': ingredients_data})

  except Exception as e:
    return JsonResponse({ 'status': 'error', 'message': f'Erro ao carregar ingredientes: {str(e)}', 'data': []}, status=500)

def meal_add(request):
  if request.method != 'POST':
    return JsonResponse({'status': 'error', 'error': '405', 'message': 'Método inválido.'}, status=405)

  if 'worker' not in request.session:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autenticado.'}, status=403)

  if request.session.get('workerRole', {}).get('permission', 0) < 4:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)

  try:
    category_id = request.POST.get('category')
    name_ = request.POST.get('name')
    description_ = request.POST.get('description')
    price_ = request.POST.get('price')
    image_file = request.FILES.get('image')

    if not category_id or not name_ or not description_ or not price_:
      return JsonResponse({'status': 'error', 'error': '400', 'message': 'Preencha todos os campos.'}, status=400)

    try:
      price_ = float(price_)
      if price_ <= 0:
        return JsonResponse({'status': 'error', 'error': '400', 'message': 'O preço não pode ser zero ou negativo.'}, status=400)
    except ValueError:
      return JsonResponse({'status': 'error', 'error': '400', 'message': 'Preço inválido.'}, status=400)

    category_ = models.Category.objects.filter(id=category_id).first()
    if not category_:
      return JsonResponse({'status': 'error', 'error': '400', 'message': 'Categoria inválida.'}, status=400)

    models.Meal.objects.create(
      category=category_,
      name=name_,
      description=description_,
      price=price_,
      image=image_file  
    )

    return JsonResponse({'status': 'success', 'message': 'Registro criado com sucesso!'})

  except Exception as e:
    return JsonResponse({'status': 'error', 'error': '500', 'message': f'Erro interno: {str(e)}'}, status=500)
  
def meal_edit(request):
  if request.method != 'POST':
    return JsonResponse({'status': 'error', 'error': '405', 'message': 'Método inválido.'}, status=405)

  if 'worker' not in request.session:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autenticado.'}, status=403)

  if request.session.get('workerRole', {}).get('permission', 0) < 4:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)

  try:
    name_ = request.POST.get('name')
    description_ = request.POST.get('description')
    price_ = request.POST.get('price')
    image_file = request.FILES.get('image')

    try:
      price_ = float(price_)
      if price_ <= 0:
        return JsonResponse({'status': 'error', 'error': '400', 'message': 'O preço não pode ser zero ou negativo.'}, status=400)
    except ValueError:
      return JsonResponse({'status': 'error', 'error': '400', 'message': 'Preço inválido.'}, status=400)

    meal = models.Meal.objects.get(id=request.POST.get('mealID'))
    meal.name = name_
    meal.description = description_
    meal.price = price_
    if image_file:
      meal.image = image_file
    meal.save()

    return JsonResponse({'status': 'success', 'message': 'Registro editado com sucesso!'})

  except Exception as e:
    return JsonResponse({'status': 'error', 'error': '500', 'message': f'Erro interno: {str(e)}'}, status=500)

def meal_data(request):
  if request.method != 'POST':
    return JsonResponse({'status': 'error', 'error': '405', 'message': 'Método inválido.'}, status=405)

  if 'worker' not in request.session:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autenticado.'}, status=403)

  if request.session.get('workerRole', {}).get('permission', 0) < 4:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)

  try:
    meal_id = request.POST.get('meal')
    meal = models.Meal.objects.get(id=meal_id)

    mealData = {
      'name' : meal.name,
      'description' : meal.description,
      'image' : request.build_absolute_uri(meal.image.url) if meal.image else None,
      'price' : meal.price,
    }

    return JsonResponse({'status': 'success', 'message': 'Infromação encontrada com sucesso!', 'mealData' : mealData})

  except Exception as e:
    return JsonResponse({'status': 'error', 'error': '500', 'message': f'Erro interno: {str(e)}'}, status=500)

def meal_remove(request):
  if request.method != 'POST':
    return JsonResponse({'status': 'error', 'error': '405', 'message': 'Método inválido.'}, status=405)

  if 'worker' not in request.session:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autenticado.'}, status=403)

  if request.session.get('workerRole', {}).get('permission', 0) < 4:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)

  try:
    meal_id = request.POST.get('meal')

    models.Meal.objects.get(id=meal_id).delete()

    return JsonResponse({'status': 'success', 'message': 'Registro removido com sucesso!'})

  except Exception as e:
    return JsonResponse({'status': 'error', 'error': '500', 'message': f'Erro interno: {str(e)}'}, status=500)

def ingredient_add(request):
  meal_ = models.Meal.objects.get(id = request.POST.get('meal'))
  ingredient_ = models.Product.objects.get(id = request.POST.get('ingredient'))

  try:

    models.Ingredient.objects.create(
      meal = meal_,
      ingredient = ingredient_,
    )

    ingredientData = {
      'id' : ingredient_.id,
      'name' : ingredient_.name,
      'quantity' : ingredient_.quantity,
      'image' : request.build_absolute_uri(ingredient_.image.url) if ingredient_.image else None,
      'mealID' : meal_.id,
    }

    return JsonResponse({'status': 'success', 'message': 'Ingrediente adicionado com sucesso!', 'ingredient' : ingredientData})
  except:
    return JsonResponse({'status': 'error', 'error': '500', 'message': 'Erro interno: '}, status=500)
  
def ingredient_increment(request):
  if request.method != 'POST':
    return JsonResponse({'status': 'error', 'error': '405', 'message': 'Método inválido.'}, status=405)

  if 'worker' not in request.session:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autenticado.'}, status=403)

  if request.session.get('workerRole', {}).get('permission', 0) < 4:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)

  data = json.loads(request.body)  
  meal_ = models.Meal.objects.get(id = data.get('meal'))
  ingredient_ = models.Product.objects.get(id = data.get('ingredient'))

  try:

    entry = models.Ingredient.objects.get(meal_id = meal_, ingredient_id = ingredient_)
    entry.quantity += 1 
    entry.save()

    return JsonResponse({'status': 'success', 'message': 'Ingrediente adicionado com sucesso!', 'quantity' : entry.quantity})
  except:
    return JsonResponse({'status': 'error', 'error': '500', 'message': 'Erro interno: '}, status=500)

def ingredient_subtract(request):
  if request.method != 'POST':
    return JsonResponse({'status': 'error', 'error': '405', 'message': 'Método inválido.'}, status=405)

  if 'worker' not in request.session:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autenticado.'}, status=403)

  if request.session.get('workerRole', {}).get('permission', 0) < 4:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)

  data = json.loads(request.body)  
  meal_ = models.Meal.objects.get(id = data.get('meal'))
  ingredient_ = models.Product.objects.get(id = data.get('ingredient'))

  try:

    entry = models.Ingredient.objects.get(meal_id = meal_, ingredient_id = ingredient_)
    entry.quantity -= 1 

    if (entry.quantity < 0):
      return JsonResponse({'status': 'error', 'error': '400', 'message': 'A quantidade não pode ser menor que zero.'}, status=400)

    entry.save()

    return JsonResponse({'status': 'success', 'message': 'Ingrediente subtraído com sucesso!', 'quantity' : entry.quantity})
  except:
    return JsonResponse({'status': 'error', 'error': '500', 'message': 'Erro interno: '}, status=500)

def ingredient_remove(request):
  if request.method != 'POST':
    return JsonResponse({'status': 'error', 'error': '405', 'message': 'Método inválido.'}, status=405)

  if 'worker' not in request.session:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autenticado.'}, status=403)

  if request.session.get('workerRole', {}).get('permission', 0) < 4:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)

  data = json.loads(request.body)  
  meal_ = models.Meal.objects.get(id = data.get('meal'))
  ingredient_ = models.Product.objects.get(id = data.get('ingredient'))

  try:

    entry = models.Ingredient.objects.get(meal_id = meal_, ingredient_id = ingredient_)
    entry.delete()

    return JsonResponse({'status': 'success', 'message': 'Ingrediente removido com sucesso!'})
  except:
    return JsonResponse({'status': 'error', 'error': '500', 'message': 'Erro interno: '}, status=500)

def categories(request):
  if 'worker' not in request.session:
    return redirect('workers:login')
  
  types = [
    (1, 'LANCHES'),
    (2, 'SOBREMESAS'),
    (3, 'PORÇÕES'),
    (4, 'BEBIDAS'),
    (5, 'PRODUTOS'),
    (6, 'INGREDIENTES'),
    (7, 'TICKETS')
  ]

  entries = {type_id: {"name": type_name, "categories": []} for type_id, type_name in types}

  for type_id, type_name in types:
    categories = models.Category.objects.filter(type=type_id)

    for category in categories:
        category_data = {
          "category_name": category.name,
          "category_id": category.id,
          "items": []
        }

        entries[type_id]["categories"].append(category_data)

  context = {
    'worker': request.session.get('worker'),
    'workerRole': request.session.get('workerRole'),
    'entries' : entries,
  }

  return render(request, 'core/categories.html', context)

def category_add(request):
  if request.method != 'POST':
    return JsonResponse({'status': 'error', 'error': '405', 'message': 'Método inválido.'}, status=405)

  if 'worker' not in request.session:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autenticado.'}, status=403)

  if request.session.get('workerRole', {}).get('permission', 0) < 4:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)

  try:
    type_ = request.POST.get('type')
    name_ = request.POST.get('name')

    if not type_ or not name_:
      return JsonResponse({'status': 'error', 'error': '400', 'message': 'Preencha todos os campos obrigatórios.'}, status=400)

    product = models.Category.objects.create(
      name=name_,
      type=type_,
    )

    return JsonResponse({'status': 'success', 'message': 'Registro criado com sucesso!', 'category_id': product.id})

  except Exception as e:
    return JsonResponse({'status': 'error', 'error': '500', 'message': f'Erro interno: {str(e)}'}, status=500)
  
def category_edit(request):
  if request.method != 'POST':
    return JsonResponse({'status': 'error', 'error': '405', 'message': 'Método inválido.'}, status=405)

  if 'worker' not in request.session:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autenticado.'}, status=403)

  if request.session.get('workerRole', {}).get('permission', 0) < 4:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)

  try:
    name_ = request.POST.get('name')

    category_ = models.Category.objects.get(id=request.POST.get('categoryID'))

    category_.name = name_
    category_.save()

    return JsonResponse({'status': 'success', 'message': 'Registro editado com sucesso!'})

  except Exception as e:
    return JsonResponse({'status': 'error', 'error': '500', 'message': f'Erro interno: {str(e)}'}, status=500)

def category_data(request):
  if request.method != 'POST':
    return JsonResponse({'status': 'error', 'error': '405', 'message': 'Método inválido.'}, status=405)

  if 'worker' not in request.session:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autenticado.'}, status=403)

  if request.session.get('workerRole', {}).get('permission', 0) < 4:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)

  try:
    category_id = request.POST.get('category')
    category = models.Category.objects.get(id=category_id)

    categoryData = {
      'name' : category.name,
    }

    return JsonResponse({'status': 'success', 'message': 'Infromação encontrada com sucesso!', 'categoryData' : categoryData})

  except Exception as e:
    return JsonResponse({'status': 'error', 'error': '500', 'message': f'Erro interno: {str(e)}'}, status=500)

def category_remove(request):
  if request.method != 'POST':
    return JsonResponse({'status': 'error', 'error': '405', 'message': 'Método inválido.'}, status=405)

  if 'worker' not in request.session:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autenticado.'}, status=403)

  if request.session.get('workerRole', {}).get('permission', 0) < 4:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)

  try:
    category_id = request.POST.get('category')

    models.Category.objects.get(id=category_id).delete()

    return JsonResponse({'status': 'success', 'message': 'Registro removido com sucesso!'})

  except Exception as e:
    return JsonResponse({'status': 'error', 'error': '500', 'message': f'Erro interno: {str(e)}'}, status=500)

def products(request):
  if 'worker' not in request.session:
    return redirect('workers:login')
  
  types = [
    (4, 'BEBIDAS'),
    (5, 'PRODUTOS'),
    (6, 'INGREDIENTES'),
  ]

  entries = {type_id: {"name": type_name, "categories": []} for type_id, type_name in types}

  for type_id, type_name in types:
    categories = models.Category.objects.filter(type=type_id)

    for category in categories:
        category_data = {
          "category_name": category.name,
          "category_id": category.id,
          "items": []
        }

        products = models.Product.objects.filter(category_id=category.id)
        for product in products:
          category_data["items"].append({
            "id": product.id,
            "name": product.name,
            "image" : product.image.url if product.image else None,
            "quantity" : product.quantity,
            "price" : product.sell_price,
          })

        entries[type_id]["categories"].append(category_data)

  context = {
    'worker': request.session.get('worker'),
    'workerRole': request.session.get('workerRole'),
    'entries' : entries,
  }

  return render(request, 'core/products.html', context)

def product_add(request):
  if request.method != 'POST':
    return JsonResponse({'status': 'error', 'error': '405', 'message': 'Método inválido.'}, status=405)

  if 'worker' not in request.session:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autenticado.'}, status=403)

  if request.session.get('workerRole', {}).get('permission', 0) < 4:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)

  try:
    category_id = request.POST.get('category')
    name_ = request.POST.get('name')
    sell_price_ = request.POST.get('price')
    image_file = request.FILES.get('image')

    if not category_id or not name_:
      return JsonResponse({'status': 'error', 'error': '400', 'message': 'Preencha todos os campos obrigatórios.'}, status=400)

    category_ = models.Category.objects.filter(id=category_id).first()
    if not category_:
      return JsonResponse({'status': 'error', 'error': '400', 'message': 'Categoria inválida.'}, status=400)

    if category_.type == 4:
      if not sell_price_:
        return JsonResponse({'status': 'error', 'error': '400', 'message': 'Preço obrigatório para esta categoria.'}, status=400)
      try:
        sell_price_ = float(sell_price_)
        if sell_price_ <= 0:
          return JsonResponse({'status': 'error', 'error': '400', 'message': 'O preço não pode ser zero ou negativo.'}, status=400)
      except ValueError:
        return JsonResponse({'status': 'error', 'error': '400', 'message': 'Preço inválido.'}, status=400)
    else:
      sell_price_ = None

    product = models.Product.objects.create(
      category=category_,
      name=name_,
      sell_price=sell_price_,
      image=image_file  
    )

    return JsonResponse({'status': 'success', 'message': 'Registro criado com sucesso!', 'product_id': product.id})

  except Exception as e:
    return JsonResponse({'status': 'error', 'error': '500', 'message': f'Erro interno: {str(e)}'}, status=500)
  
def product_edit(request):
  if request.method != 'POST':
    return JsonResponse({'status': 'error', 'error': '405', 'message': 'Método inválido.'}, status=405)

  if 'worker' not in request.session:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autenticado.'}, status=403)

  if request.session.get('workerRole', {}).get('permission', 0) < 4:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)

  try:
    name_ = request.POST.get('name')
    sell_price_ = request.POST.get('price')
    image_file = request.FILES.get('image')

    product = models.Product.objects.get(id=request.POST.get('productID'))
    category_ = product.category

    if category_.type == 4:
      if not sell_price_:
        return JsonResponse({'status': 'error', 'error': '400', 'message': 'Preço obrigatório para esta categoria.'}, status=400)
      try:
        sell_price_ = float(sell_price_)
        if sell_price_ <= 0:
          return JsonResponse({'status': 'error', 'error': '400', 'message': 'O preço não pode ser zero ou negativo.'}, status=400)
      except ValueError:
        return JsonResponse({'status': 'error', 'error': '400', 'message': 'Preço inválido.'}, status=400)
    else:
      sell_price_ = None

    product.name = name_
    product.sell_price = sell_price_
    if image_file:
      product.image = image_file
    product.save()

    return JsonResponse({'status': 'success', 'message': 'Registro editado com sucesso!'})

  except Exception as e:
    return JsonResponse({'status': 'error', 'error': '500', 'message': f'Erro interno: {str(e)}'}, status=500)

def product_data(request):
  if request.method != 'POST':
    return JsonResponse({'status': 'error', 'error': '405', 'message': 'Método inválido.'}, status=405)

  if 'worker' not in request.session:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autenticado.'}, status=403)

  if request.session.get('workerRole', {}).get('permission', 0) < 4:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)

  try:
    product_id = request.POST.get('product')
    product = models.Product.objects.get(id=product_id)

    productData = {
      'name' : product.name,
      'image' : request.build_absolute_uri(product.image.url) if product.image else None,
      'price' : product.sell_price,
    }

    return JsonResponse({'status': 'success', 'message': 'Infromação encontrada com sucesso!', 'productData' : productData})

  except Exception as e:
    return JsonResponse({'status': 'error', 'error': '500', 'message': f'Erro interno: {str(e)}'}, status=500)

def product_remove(request):
  if request.method != 'POST':
    return JsonResponse({'status': 'error', 'error': '405', 'message': 'Método inválido.'}, status=405)

  if 'worker' not in request.session:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autenticado.'}, status=403)

  if request.session.get('workerRole', {}).get('permission', 0) < 4:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)

  try:
    product_id = request.POST.get('product')

    models.Product.objects.get(id=product_id).delete()

    return JsonResponse({'status': 'success', 'message': 'Registro removido com sucesso!'})

  except Exception as e:
    return JsonResponse({'status': 'error', 'error': '500', 'message': f'Erro interno: {str(e)}'}, status=500)
