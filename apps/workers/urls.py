from django.urls import path
from . import views

app_name = 'workers'
urlpatterns = [
    path('', views.index, name='index'),
    path("get-shift/", views.get_shift, name="get-shift"),
    path('login/', views.login, name='login'),
    path('login/authentication/', views.authentication, name='authentication'),
    path('logout/', views.logout, name='logout'),
]