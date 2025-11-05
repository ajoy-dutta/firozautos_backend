from rest_framework.routers import DefaultRouter
from .views import (
    ProductCategoryViewSet, ProductViewSet, BikeModelViewSet,
    SupplierPurchaseViewSet, StockViewSet, SupplierPurchaseReturnViewSet,
    OrderViewSet
)

router = DefaultRouter()
router.register(r'product-categories', ProductCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'bike-models', BikeModelViewSet)  # ✅ NEW
router.register(r'supplier-purchases', SupplierPurchaseViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'supplier-purchase-returns', SupplierPurchaseReturnViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = router.urls
