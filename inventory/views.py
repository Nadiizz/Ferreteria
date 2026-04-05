import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Count, Sum
from .models import Product, Supplier, Customer, Sale, SaleItem
from .forms import ProductForm
from django.utils import timezone
import datetime

def dashboard_view(request):
    # Calculate metrics for the dashboard
    all_products = Product.objects.all()
    total_products = all_products.count()
    low_stock_count = all_products.filter(status='low-stock').count()
    out_stock_count = all_products.filter(status='out-stock').count()
    alert_count = low_stock_count + out_stock_count

    # Category Distribution for Doughnut Chart
    category_counts = all_products.values('category').annotate(count=Count('id'))
    category_labels = [item['category'] for item in category_counts]
    category_data = [item['count'] for item in category_counts]

    # Monthly Sales for Bar Chart
    now = timezone.now()
    six_months_ago = now - datetime.timedelta(days=180)
    recent_sales = Sale.objects.filter(date__gte=six_months_ago, status='completed')
    
    # Group in python to be DB agnostic (SQLite friendly)
    monthly_sales = {}
    for i in range(6):
        m = (now - datetime.timedelta(days=30*i)).strftime('%Y-%m')
        monthly_sales[m] = {'ingresos': 0, 'salidas': 0}
        
    for sale in recent_sales:
        month_key = sale.date.strftime('%Y-%m')
        if month_key in monthly_sales:
            monthly_sales[month_key]['ingresos'] += float(sale.total)

    # Sort months chronologically
    sorted_months = sorted(monthly_sales.keys())
    sales_labels = sorted_months
    sales_ingresos_data = [monthly_sales[m]['ingresos'] for m in sorted_months]
    sales_salidas_data = [monthly_sales[m]['ingresos'] * 0.4 for m in sorted_months] # Simulación salidas 40%

    context = {
        'active_page': 'dashboard',
        'total_products': total_products,
        'alert_count': alert_count,
        'category_labels': category_labels,
        'category_data': category_data,
        'sales_labels': sales_labels,
        'sales_ingresos_data': sales_ingresos_data,
        'sales_salidas_data': sales_salidas_data,
    }
    return render(request, 'inventory/dashboard.html', context)

def products_view(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(sku__icontains=query) | 
            Q(name__icontains=query) | 
            Q(category__icontains=query)
        )
    else:
        products = Product.objects.all()
        
    context = {
        'active_page': 'products',
        'products': products,
        'query': query,
    }
    return render(request, 'inventory/products.html', context)

def sales_view(request):
    sales = Sale.objects.all().order_by('-date')
    context = {
        'active_page': 'sales',
        'sales': sales
    }
    return render(request, 'inventory/sales.html', context)

def suppliers_view(request):
    suppliers = Supplier.objects.all().order_by('name')
    context = {
        'active_page': 'suppliers',
        'suppliers': suppliers
    }
    return render(request, 'inventory/suppliers.html', context)

def database_view(request):
    return render(request, 'inventory/database.html', {'active_page': 'database'})

def security_view(request):
    return render(request, 'inventory/security.html', {'active_page': 'security'})

def settings_view(request):
    return render(request, 'inventory/settings.html', {'active_page': 'settings'})

def api_save_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        if product_id:
            product = get_object_or_404(Product, id=product_id)
            form = ProductForm(request.POST, instance=product)
        else:
            form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'invalid method'}, status=400)

def api_delete_product(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=pk)
        product.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'invalid method'}, status=400)
