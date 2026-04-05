import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acme_erp.settings')
django.setup()

from inventory.models import Product, Supplier, Customer, Sale, SaleItem
from django.utils import timezone
from datetime import timedelta
import random

inventory_data = [
    { "sku": "HER-001", "name": "Taladro Percutor Bosch 800W", "category": "Herramientas Eléctricas", "location": "Pasillo 4, Estante A", "stock": 15 },
    { "sku": "HER-042", "name": "Set Destornilladores 24 pzas", "category": "Herramientas Manuales", "location": "Pasillo 2, Estante B", "stock": 4 },
    { "sku": "CON-105", "name": "Cemento Portland 25kg", "category": "Materiales de Construcción", "location": "Bodega Principal", "stock": 150 },
    { "sku": "PLO-022", "name": "Tubería PVC 20mm x 3m", "category": "Plomería", "location": "Patio Exterior", "stock": 0 },
    { "sku": "ELE-088", "name": "Cable Cobre THHN 12 AWG (100m)", "category": "Electricidad", "location": "Pasillo 6, Estante C", "stock": 12 },
    { "sku": "PIN-015", "name": "Pintura Látex Blanca 1 Galón", "category": "Pinturas", "location": "Pasillo 1, Estante A", "stock": 3 },
    { "sku": "TOR-050", "name": "Tornillos Madera 8x2\" (Caja 100)", "category": "Ferretería General", "location": "Pasillo 3, Estante D", "stock": 45 }
]

def seed():
    # 1. Products
    print("Repoblando Productos...")
    products = []
    for item in inventory_data:
        prod, created = Product.objects.get_or_create(sku=item['sku'], defaults={
            'name': item['name'],
            'category': item['category'],
            'location': item['location'],
            'stock': item['stock']
        })
        prod.save()
        products.append(prod)
    
    # 2. Suppliers
    print("Repoblando Proveedores...")
    Supplier.objects.get_or_create(tax_id="76.432.112-K", defaults={"name": "Herramientas Industriales BOSCH", "contact": "María López (+12345678)", "category": "Herramientas Eléctricas", "rating": 5, "account_status": "Al día"})
    Supplier.objects.get_or_create(tax_id="88.111.222-3", defaults={"name": "Tornillos y Acero C.A.", "contact": "Juan Pérez", "category": "Fijaciones", "rating": 3, "account_status": "Deuda $500"})
    Supplier.objects.get_or_create(tax_id="99.222.333-4", defaults={"name": "Cementos Nacionales S.A.", "contact": "Pedro Gómez", "category": "Construcción", "rating": 4, "account_status": "Al día"})

    # 3. Customers
    print("Repoblando Clientes...")
    c1, _ = Customer.objects.get_or_create(name="Constructora del Sur S.A.", defaults={"customer_type": "Mayorista"})
    c2, _ = Customer.objects.get_or_create(name="Cliente Final (Mostrador)", defaults={"customer_type": "Mostrador"})
    c3, _ = Customer.objects.get_or_create(name="Municipio Local - Obras", defaults={"customer_type": "Gobierno"})

    # 4. Sales & SaleItems (Simular datos historicos para el Dashboard)
    print("Repoblando Ventas...")
    if Sale.objects.count() == 0:
        customers = [c1, c2, c3]
        methods = ['Efectivo', 'Transferencia', 'Cheque', 'Tarjeta de Crédito']
        now = timezone.now()
        
        # Crear 50 ventas en los últimos 6 meses
        for i in range(50):
            customer = random.choice(customers)
            method = random.choice(methods)
            days_ago = random.randint(0, 180)
            sale_date = now - timedelta(days=days_ago)
            
            # Crear venta
            s = Sale.objects.create(
                order_number=f"ORD-{sale_date.year}-9{100+i}",
                customer=customer,
                payment_method=method,
                status=random.choices(['completed', 'pending', 'cancelled'], weights=[80, 15, 5])[0]
            )
            
            # Modificar la fecha insertada automáticamente
            Sale.objects.filter(id=s.id).update(date=sale_date)
            
            # Añadir items ficticios
            num_items = random.randint(1, 4)
            total = 0
            for _ in range(num_items):
                prod = random.choice(products)
                qty = random.randint(1, 5)
                price = random.uniform(5.0, 100.0)
                SaleItem.objects.create(sale=s, product=prod, quantity=qty, price=price)
                total += qty * price
                
            # Actualizar total
            Sale.objects.filter(id=s.id).update(total=total)

    print("Base de datos generada exitosamente. ¡Datos listos!")

if __name__ == '__main__':
    seed()
