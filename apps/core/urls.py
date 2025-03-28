# ============================================================
# IMPORTS - Modules used in the routes
# ============================================================

# Django Modules
from django.urls import path

# Project Modules
from . import views

# ============================================================
# ROUTES - Routes to the defs
# ============================================================

# App Name
app_name = 'core'

# URL Patterns
urlpatterns = [

  # Index page(manage)
  path('', views.index, name='index'),

  # Stock system
  path('stock/', views.stock, name='stock'),
  path('stock/edit/get-products/', views.get_products, name="get-products"),
  path('stock/edit/load-product/<int:id>/', views.load_product, name="load-product"),
  path('stock/edit/save/<int:id>/', views.stock_edit_save, name='stock-edit-save'),
  path('stock/add/', views.stock_add, name='stock-add'),
  path('stock/remove/<int:id>/', views.stock_remove, name='stock-remove'),

  # Meal system
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

  # Category system
  path('categories/', views.categories, name='categories'),
  path('categories/add/', views.category_add, name="category-add"),
  path('categories/data/', views.category_data, name="category-data"),
  path('categories/edit/', views.category_edit, name="category-edit"),
  path('categories/remove/', views.category_remove, name="category-remove"),

  # Products system
  path('products/', views.products, name='products'),
  path('products/add/get-categories/<int:id>/', views.get_categories, name="get-categories"),
  path('products/add/', views.product_add, name="product-add"),
  path('products/data/', views.product_data, name="product-data"),
  path('products/edit/', views.product_edit, name="product-edit"),
  path('products/remove/', views.product_remove, name="product-remove"),

  # Ticket system
  path('tickets/', views.tickets, name="tickets"),
  path('tickets/add/', views.ticket_add, name="ticket-add"),
  path('tickets/status/', views.ticket_status, name="ticket-status"),
  path('tickets/remove/', views.ticket_remove, name="ticket-remove"),

  # Sale system
  path('sales/', views.sales, name="sales"),
  path('sales/add/', views.sale_add, name="sale-add"),
  path('sales/remove/', views.sale_remove, name="sale-remove"),

  # Supplier system
  path('suppliers/', views.suppliers, name="suppliers"),
  path('suppliers/add/', views.supplier_add, name="supplier-add"),
  path('suppliers/edit/', views.supplier_edit, name="supplier-edit"),
  path('suppliers/data/', views.supplier_data, name="supplier-data"),
  path('suppliers/remove/', views.supplier_remove, name="supplier-remove"),

]