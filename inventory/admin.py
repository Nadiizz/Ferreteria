from django.contrib import admin
from .models import Product, Supplier, Customer, Sale, SaleItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'location', 'stock', 'status')
    search_fields = ('sku', 'name', 'category')
    list_filter = ('status', 'category')
    readonly_fields = ('status',) # Status auto-calculates on save

admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(Sale)
admin.site.register(SaleItem)
