from django.db import models

class Product(models.Model):
    STATUS_CHOICES = [
        ('in-stock', 'En Stock'),
        ('low-stock', 'Stock Bajo'),
        ('out-stock', 'Agotado'),
    ]

    sku = models.CharField("SKU", max_length=20, unique=True)
    name = models.CharField("Nombre", max_length=150)
    category = models.CharField("Categoría", max_length=100)
    location = models.CharField("Ubicación", max_length=100)
    stock = models.IntegerField("Stock", default=0)
    status = models.CharField("Estado", max_length=20, choices=STATUS_CHOICES, default='in-stock')

    def save(self, *args, **kwargs):
        # Auto-update status based on stock level if we want
        # but let's just make it simple:
        if self.stock <= 0:
            self.status = 'out-stock'
        elif self.stock <= 5:
            self.status = 'low-stock'
        else:
            self.status = 'in-stock'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sku} - {self.name}"

    class Meta:
        verbose_name = "Producto / Insumo"
        verbose_name_plural = "Productos / Insumos"
        ordering = ['name']

class Supplier(models.Model):
    name = models.CharField("Razón Social", max_length=150)
    tax_id = models.CharField("RUT/NIT", max_length=50, unique=True)
    contact = models.CharField("Contacto (Nombre y Tel)", max_length=150)
    category = models.CharField("Categoría Suministro", max_length=100)
    rating = models.IntegerField("Rating", default=3) # 1 a 5
    account_status = models.CharField("Estado de Cuenta", max_length=100, default="Al día")
    
    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField("Razón Social / Nombre", max_length=150)
    customer_type = models.CharField("Tipo", max_length=50, default="Mostrador")
    
    def __str__(self):
        return self.name

class Sale(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completado'),
        ('pending', 'Por Aprobar'),
        ('cancelled', 'Cancelada'),
    ]
    order_number = models.CharField("Nº Orden", max_length=30, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField("Método Pago", max_length=50)
    total = models.DecimalField("Total", max_digits=10, decimal_places=2, default=0.00)
    date = models.DateTimeField("Fecha", auto_now_add=True)
    status = models.CharField("Estado", max_length=20, choices=STATUS_CHOICES, default='completed')

    def __str__(self):
        return self.order_number

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField("Cantidad")
    price = models.DecimalField("Precio Unitario", max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
