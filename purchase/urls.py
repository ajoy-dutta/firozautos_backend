from rest_framework.routers import DefaultRouter
from .views import (
    SupplierPurchaseViewSet, SupplierPurchaseReturnViewSet,
    OrderViewSet, UploadStockExcelView
)
from django.urls import path, include

router = DefaultRouter()
router.register(r'supplier-purchases', SupplierPurchaseViewSet)
router.register(r'supplier-purchase-returns', SupplierPurchaseReturnViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload-order-excel/', UploadStockExcelView.as_view(), name='upload-stock-excel'),
]