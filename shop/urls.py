from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/products/', views.dashboard_products, name='dashboard_products'),
    path('dashboard/orders/', views.dashboard_orders, name='dashboard_orders'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]
