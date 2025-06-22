from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import*

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'product-categories', ProductCategoryViewSet)
router.register(r'products', ProductViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
