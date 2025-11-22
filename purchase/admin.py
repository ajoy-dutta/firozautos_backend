from django.contrib import admin
from .models import *


admin.site.register(PurchaseProduct)
admin.site.register(PurchasePayment)
admin.site.register(SupplierPurchase)
admin.site.register(SupplierPurchaseReturn)
admin.site.register(Purchase)
admin.site.register(PurchaseItem)
# Orders (minimal, same style)
admin.site.register(Order)
admin.site.register(OrderItem)
