from django.contrib import admin
from .models import Sale, SaleProduct, SalePayment, SaleReturn

admin.site.register(Sale)
admin.site.register(SaleProduct)
admin.site.register(SalePayment)
admin.site.register(SaleReturn)
