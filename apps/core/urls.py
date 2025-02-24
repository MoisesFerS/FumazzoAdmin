from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('stock/', views.stock, name='stock'),
    path('stock/edit/get-products/', views.get_products, name="get-products"),
    path('stock/edit/load-product/<int:id>/', views.load_product, name="load-product"),
    path('stock/edit/save/<int:id>/', views.stock_edit_save, name='stock-edit-save'),
    path('stock/add/', views.stock_add, name='stock-add'),
    path('stock/remove/<int:id>/', views.stock_remove, name='stock-remove'),
    path('register/category/', views.category, name='category'),
    path('register/supplier/', views.supplier, name='supplier'),
    path('register/product/', views.product, name='product'),
    path('register/meal/', views.meal, name='meal'),
]