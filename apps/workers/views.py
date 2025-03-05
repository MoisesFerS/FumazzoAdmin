from django.shortcuts import render, redirect
from . import models
from .utils import bcrypt
from django.http import JsonResponse
import json
from django.db.models import Count, Max, Q
from apps.core.models import Category

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
	shift = worker.shift	
	shift_end = str(shift.end_time)

	workerData = {
		'sector_id' : sector.id,
		'sector_name' : sector.name,
		'description' : role.description,
		'image': role.image.url if role.image else None,
		'shift_end' : shift_end,
	}

	notifications = models.Notification.objects.filter(sector_id = workerData['sector_id'])
	sectors = models.Sector.objects.annotate(
			ticket_count=Count('ticket', filter=~Q(ticket__status=3)),
			max_priority=Max('ticket__priority', filter=~Q(ticket__status=3)) 
	)

	tickets_categories = Category.objects.filter(type=6)

	context = {
		'worker': request.session.get('worker'),
		'workerRole': request.session.get('workerRole'),
		'workerData' : workerData,
		'notifications' : notifications,
		'sectors' : sectors,
		'tickets_categories' : tickets_categories,
	}
	
	return render(request, 'workers/index.html', context)

#   ============================================================
#   LOGIN - Defs related to User login
#   ============================================================ 

# Renders the Login page
def login(request):
	return render(request, 'workers/login.html')

# Authenticates the user
def authentication(request):

	if request.method != 'POST':
		return JsonResponse({'status': 'error', 'error' : '405', 'message': 'Método inválido.'}, status=405)	

	try:

		data = json.loads(request.body)

		if not data.get('id') or not data.get('password'):
			return JsonResponse({'status': 'error', 'error' : '400', 'message': 'ID e senha são obrigatórios.'}, status=400)

		try:
			worker = models.Worker.objects.get(id = data.get('id'))
		except:
			return JsonResponse({'status': 'error', 'error' : '400', 'message': 'Credenciais inválidas.'}, status=400)

		if bcrypt.checkpw(data.get('password').encode('UTF-8'), worker.password.encode('UTF-8')):

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
			return JsonResponse({'status': 'error', 'error' : '400', 'message': 'Credenciais inválidas.'}, status=400)

	except json.JSONDecodeError:
		return JsonResponse({'status': 'error', 'error' : '400', 'message': 'Erro ao processar JSON'}, status=400)
	

def authentication(request):
	if request.method != 'POST':
		return JsonResponse({'status': 'error', 'error': '405', 'message': 'Método inválido.'}, status=405)

	try:
		data = json.loads(request.body)

		if not data.get('id') or not data.get('password'):
			return JsonResponse({'status': 'error', 'error': '400', 'message': 'ID e senha são obrigatórios.'}, status=400)

		try:
			worker = models.Worker.objects.get(id=data.get('id'))
		except models.Worker.DoesNotExist:
			return JsonResponse({'status': 'error', 'error': '400', 'message': 'Credenciais inválidas.'}, status=400)
		
		if bcrypt.checkpw(data.get('password').encode('UTF-8'), worker.password.encode('UTF-8')):

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