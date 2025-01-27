from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('stock/', views.stock, name='stock'),
    path('stock/restock/', views.restock, name='restock'),
    path('stock/restock/delete/<int:id>/', views.restock_delete, name='restock_delete'),
    path('register/category/', views.category, name='category'),
    path('register/supplier/', views.supplier, name='supplier'),
    path('register/product/', views.product, name='product'),
    path('register/meal/', views.meal, name='meal'),
]