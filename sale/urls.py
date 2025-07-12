from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SaleViewSet, SaleReturnViewSet

router = DefaultRouter()
router.register(r'sales', SaleViewSet, basename='sale')
router.register(r'sale-returns', SaleReturnViewSet, basename='sale-return')

urlpatterns = [
    path('', include(router.urls)),
] 