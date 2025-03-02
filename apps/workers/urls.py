from django.urls import path
from . import views

app_name = 'workers'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('login/authentication/', views.authentication, name='authentication'),
    path('logout/', views.logout, name='logout'),
]