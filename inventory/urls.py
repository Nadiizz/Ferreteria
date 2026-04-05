from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('products/', views.products_view, name='products'),
    path('sales/', views.sales_view, name='sales'),
    path('suppliers/', views.suppliers_view, name='suppliers'),
    path('database/', views.database_view, name='database'),
    path('security/', views.security_view, name='security'),
    path('settings/', views.settings_view, name='settings'),
    
    # APIs
    path('api/save/', views.api_save_product, name='api_save'),
    path('api/delete/<int:pk>/', views.api_delete_product, name='api_delete'),
]
