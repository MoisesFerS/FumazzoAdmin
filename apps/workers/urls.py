from django.urls import path
from . import views

urlpatterns = [
    path('', views.workers_index, name=('workers_index')),
]