from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-product/', views.add_product, name='add_product'),
    path('products/', views.view_products, name='view_products'),
]
