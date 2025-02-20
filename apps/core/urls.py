from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('stock/', views.stock, name='stock'),
    path('stock/restock/edit/get-products/', views.get_products, name="get-products"),
    path('stock/restock/edit/load-product/<int:id>/', views.load_product, name="load-product"),
    path('stock/restock/add/', views.restock_add, name='restock'),
    path('stock/restock/remove/<int:id>/', views.restock_remove, name='restock_remove'),
    path('register/category/', views.category, name='category'),
    path('register/supplier/', views.supplier, name='supplier'),
    path('register/product/', views.product, name='product'),
    path('register/meal/', views.meal, name='meal'),
]