from rest_framework import viewsets
from .models import*
from .serializers import*
from rest_framework.permissions import IsAuthenticatedOrReadOnly



class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.select_related('company').all()
    serializer_class = ProductCategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer




class SupplierPurchaseViewSet(viewsets.ModelViewSet):
    queryset = SupplierPurchase.objects.all().order_by('-purchase_date')
    serializer_class = SupplierPurchaseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



class StockViewSet(viewsets.ModelViewSet):
    queryset = StockProduct.objects.all()
    serializer_class = StockSerializer