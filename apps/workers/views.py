from django.shortcuts import render, redirect
from . import models
from .utils import bcrypt
from django.http import JsonResponse
import json
from django.db.models import Count, Max, Q
from apps.core.models import Category
from apps.core.views import validation_insert

#   ============================================================
#   INDEX - Defs related to Index page(dashboard)
#   ============================================================ 

# Renders the Index page
def index(request):

	if 'worker' not in request.session:
		return redirect('workers:login')

	worker = models.Worker.objects.get(id = request.session['worker']['id'])
	role = worker.role
	sector = role.sector

	workerData = {
		'sector_id' : sector.id,
		'sector_name' : sector.name,
		'description' : role.description,
		'image': role.image.url if role.image else None,
	}

	notifications = models.Notification.objects.filter(Q(sector_id=workerData['sector_id']) | Q(sector_id__isnull=True))
	sectors = models.Sector.objects.annotate(
			ticket_count=Count('ticket', filter=~Q(ticket__status=3)),
			max_priority=Max('ticket__priority', filter=~Q(ticket__status=3)) 
	)

	tickets_categories = Category.objects.filter(type=7)

	context = {
		'worker': request.session.get('worker'),
		'workerRole': request.session.get('workerRole'),
		'workerData' : workerData,
		'notifications' : notifications,
		'sectors' : sectors,
		'tickets_categories' : tickets_categories,
	}
	
	return render(request, 'workers/index.html', context)

# Retrieves the user shift information
def get_shift(request):

	worker = models.Worker.objects.get(id = request.session['worker']['id'])
	shift = worker.shift

	data = {
		'start' : shift.start_time,
		'end' : shift.end_time,
		'name' : shift.name
	}

	return JsonResponse(data, safe=False)

#   ============================================================
#   LOGIN - Defs related to User login
#   ============================================================ 

# Renders the Login page
def login(request):
	return render(request, 'workers/login.html')

# Authenticates the user
def authentication(request):
  if request.method != 'POST':
    return JsonResponse({'status': 'error', 'error': '405', 'message': 'Método inválido.'}, status=405)

  try:

    if not request.POST.get('id') or not request.POST.get('password'):
      return JsonResponse({'status': 'error', 'error': '400', 'message': 'ID e senha são obrigatórios.'}, status=400)        

    try:
      worker = models.Worker.objects.get(id=request.POST.get('id'))
    except models.Worker.DoesNotExist:
      return JsonResponse({'status': 'error', 'error': '400', 'message': 'Credenciais inválidas.'}, status=400)

    if bcrypt.checkpw(request.POST.get('password').encode('UTF-8'), worker.password.encode('UTF-8')):

      role = worker.role

      request.session['worker'] = {
        'id': worker.id,
        'first_name': worker.first_name,
        'last_name': worker.last_name,
      }
      request.session['workerRole'] = {
        'permission': role.permission,
        'name': role.name,
      }

      return JsonResponse({'status': 'success', 'message': 'Login realizado com sucesso!', 'redirect_url': '/workers/'})

    else:
      return JsonResponse({'status': 'error', 'error': '400', 'message': 'Credenciais inválidas.'}, status=400)

  except json.JSONDecodeError:
    return JsonResponse({'status': 'error', 'error': '400', 'message': 'Erro ao processar JSON.'}, status=400)

# Flushes the session
def logout(request):
	
	request.session.flush()
	return redirect('workers:login')

#   ============================================================
#   NOTIFICATIONS - Defs related to Notification system
#   ============================================================ 

# Renders the Notification page
def notifications(request):
	
  if 'worker' not in request.session:
    return redirect('workers:login')

  if request.session.get('workerRole', {}).get('permission', 0) < 4:
    return JsonResponse({'status': 'error', 'error': '403', 'message': 'Usuário não autorizado. Permissão insuficiente.'}, status=403)

  sectors = models.Sector.objects.all()
  entries = {sector.id: {'name': sector.name, 'notifications': []} for sector in sectors}

  for sector in sectors:

    notifications = models.Notification.objects.filter(sector_id=sector.id)  

    for notification in notifications:
      notificationsData = {
        "id": notification.id,
        "message": notification.message,
        "sector" : notification.sector,
				"sender" : notification.sender,
				"date" : notification.date,
      }

      entries[sector.id]["notifications"].append(notificationsData)

  general = models.Notification.objects.filter(sector_id=None)

  entries[0] = {
    "name": "GERAL",
    "notifications": []
  }

  for notification in general:

    general_data = {
      "id": notification.id,
      "message": notification.message,
      "sector" : notification.sector,
      "sender" : notification.sender,
      "date" : notification.date,
    }

    entries[0]['notifications'].append(general_data)

  context = {
    'worker': request.session.get('worker'),
    'workerRole': request.session.get('workerRole'),
    'entries' : entries,
		"sectors" : sectors,
  }

  return render(request, 'workers/notifications.html', context)

def notification_add(request):
	
  validation_response = validation_insert(request)
  if validation_response:  
    return validation_response

  try:

    if not request.POST.get('message'):
      return JsonResponse({'status': 'error', 'error': '400', 'message': 'Preencha todos os campos.'}, status=400)

    if request.POST.get('sector') == 'null' or '':
      sector_ = None
    else:
      sector_ = models.Sector.objects.get(id = request.POST.get('sector'))

    sender_ = models.Worker.objects.get(id = request.POST.get('sender'))
    message_ = request.POST.get('message')

    models.Notification.objects.create(
      sender = sender_,
      sector = sector_,
      message = message_,
    )

    return JsonResponse({'status': 'success', 'message': 'Registro alterado com sucesso!'})

  except json.JSONDecodeError:
    return JsonResponse({'status': 'error', 'error': '400', 'message': 'Erro ao processar JSON'}, status=400)

# Retrieves the notification data
def notification_data(request):

  try:
    notification_id = request.POST.get('notification')
    notification = models.Notification.objects.get(id=notification_id)
    if notification.sector:
      sector = notification.sector.id
    else:
      sector = None

    notificationData = {
      'message' : notification.message,
      'sector' : sector
    }

    return JsonResponse({'status': 'success', 'message': 'Infromação encontrada com sucesso!', 'notificationData' : notificationData})

  except Exception as e:
    return JsonResponse({'status': 'error', 'error': '500', 'message': f'Erro interno: {str(e)}'}, status=500)

def notification_edit(request):
  
  validation_response = validation_insert(request)
  if validation_response:  
    return validation_response

  try:
    message_ = request.POST.get('message')
    sector_ = models.Sector.objects.get(id=request.POST.get('sector'))

    notification = models.Notification.objects.get(id=request.POST.get('notificationID'))
    notification.message = message_
    notification.sector = sector_

    notification.save()

    return JsonResponse({'status': 'success', 'message': 'Registro editado com sucesso!'})

  except Exception as e:
    return JsonResponse({'status': 'error', 'error': '500', 'message': f'Erro interno: {str(e)}'}, status=500)


def notification_remove(request):

  validation_response = validation_insert(request)
  if validation_response:  
    return validation_response
  
  try:
    notification_id = request.POST.get('notification')

    models.Notification.objects.get(id = notification_id).delete()

    return JsonResponse({'status': 'success', 'message': 'Registro removido com sucesso!'})

  except Exception as e:
    return JsonResponse({'status': 'error', 'error': '500', 'message': f'Erro interno: {str(e)}'}, status=500)
  