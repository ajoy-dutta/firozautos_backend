from django.contrib import admin
from .models import *

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(PurchaseProduct)
admin.site.register(PurchasePayment)
admin.site.register(SupplierPurchase)
admin.site.register(StockProduct)
admin.site.register(SupplierPurchaseReturn)

# Orders (minimal, same style)
admin.site.register(Order)
admin.site.register(OrderItem)
