from django.shortcuts import render

def workers_index(request):
    return render(request, 'workers/index.html')