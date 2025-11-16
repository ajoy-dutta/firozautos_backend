from django.contrib import admin
from .models import *

admin.site.register(Loan)
admin.site.register(Expense)
admin.site.register(Income)
admin.site.register(Purchase)
admin.site.register(PurchaseItem)