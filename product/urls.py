from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import*

router = DefaultRouter()
router.register('product-categories', ProductCategoryViewSet)
router.register('products', ProductViewSet)
router.register(r'supplier-purchases', SupplierPurchaseViewSet, basename='supplier-purchase')
router.register(r'stocks', StockViewSet)
router.register(r'supplier-purchase-returns', SupplierPurchaseReturnViewSet, basename='supplier-purchase-return')
router.register('orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]