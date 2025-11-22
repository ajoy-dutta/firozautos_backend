from rest_framework.routers import DefaultRouter
from .views import (
    ProductCategoryViewSet, ProductViewSet, BikeModelViewSet,StockViewSet,

)

router = DefaultRouter()
router.register(r'product-categories', ProductCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'bike-models', BikeModelViewSet)  # ✅ NEW
router.register(r'stocks', StockViewSet)

urlpatterns = router.urls
