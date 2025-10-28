from django.contrib import admin
from .models import*
# Register your models here.

admin.site.register(Company)
admin.site.register(CostCategory)
admin.site.register(SourceCategory)
admin.site.register(PaymentMode)
admin.site.register(DistrictMaster)
admin.site.register(CountryMaster)
admin.site.register(SupplierTypeMaster)
admin.site.register(BankCategoryMaster)
admin.site.register(BankMaster)
admin.site.register(AccountCategory)
admin.site.register(BankAccount)




