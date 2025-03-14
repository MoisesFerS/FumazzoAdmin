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
    path('meal/', views.meal, name='meal'),
    path('meal/get-ingredients/', views.get_ingredients, name="get-ingredients"),
    path('meal/add/get-categories/<int:id>/', views.get_categories, name="get-categories"),
    path('meal/add/', views.meal_add, name="meal-add"),
    path('meal/data/', views.meal_data, name="meal-data"),
    path('meal/edit/', views.meal_edit, name="meal-edit"),
    path('meal/remove/', views.meal_remove, name="meal-remove"),
    path('meal/ingredient/add/', views.ingredient_add, name="ingredient-add"),
    path('meal/ingredient/increment/', views.ingredient_increment, name="ingredient-increment"),
    path('meal/ingredient/subtract/', views.ingredient_subtract, name="ingredient-subtract"),
    path('meal/ingredient/remove/', views.ingredient_remove, name="ingredient-remove"),
    path('categories/', views.categories, name='categories'),
    path('products/', views.products, name='products'),
    path('ticket/add/', views.ticket_add, name="ticket-add"),
    path('teste/', views.teste, name='teste'),
]