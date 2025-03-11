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
    path('ticket/add/', views.ticket_add, name="ticket-add"),
    path('meal/', views.meal, name='meal'),
    path('meal/add/get-categories/<int:id>/', views.get_categories, name="get-categories"),
    path('meal/add/', views.meal_add, name="meal-add"),
    path('meal/remove/', views.meal_remove, name="meal-remove"),
    path('meal/<int:mealID>/ingredient-add/<int:ingredientID>/', views.ingredient_add, name="ingredient-add"),
    path('meal/<int:mealID>/ingredient-remove/<int:ingredientID>/', views.ingredient_remove, name="ingredient-remove"),
    path('register/category/', views.category, name='category'),
    path('register/supplier/', views.supplier, name='supplier'),
    path('register/product/', views.product, name='product'),
]