from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import*

router = DefaultRouter()
router.register('product-categories', ProductCategoryViewSet)
router.register('products', ProductViewSet)
router.register(r'supplier-purchases', SupplierPurchaseViewSet, basename='supplier-purchase')

urlpatterns = [
    path('', include(router.urls)),
]