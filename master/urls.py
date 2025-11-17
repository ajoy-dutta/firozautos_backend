from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import*

router = DefaultRouter()
router.register('companies', CompanyViewSet)
router.register('cost-categories', CostCategoryViewSet)
router.register('source-categories', SourceCategoryViewSet)
router.register('payment-mode', PaymentModeViewSet)
router.register('divisions', DivisionMasterViewSet)
router.register('districts', DistrictMasterViewSet)
router.register('countries', CountryMasterViewSet)
router.register('supplier-types', SupplierTypeMasterViewSet)
router.register('bank-categories', BankCategoryMasterViewSet)
router.register('banks', BankMasterViewSet)
router.register('account-categories', AccountCategoryViewSet)
router.register('bank-accounts', BankAccountViewSet)


urlpatterns = [
    path('', include(router.urls)),
]