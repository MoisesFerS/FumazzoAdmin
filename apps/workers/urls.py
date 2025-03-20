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
app_name = 'workers'

# URL Patterns
urlpatterns = [

	# Index page(dashboard)
	path('', views.index, name='index'),
	path('get-shift/', views.get_shift, name='get-shift'),

	# Session system
	path('login/', views.login, name='login'),
	path('login/authentication/', views.authentication, name='authentication'),
	path('logout/', views.logout, name='logout'),

	# Notification system
  path('notifications/', views.notifications, name='notifications'),
  path('notifications/add/', views.notification_add, name="notification-add"),
  path('notifications/edit/', views.notification_edit, name="notification-edit"),
  path('notifications/remove/', views.notification_remove, name="notification-remove"),

]