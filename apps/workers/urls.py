from django.urls import path
from . import views

app_name = 'workers'
urlpatterns = [
    path('', views.index, name=('index')),
]