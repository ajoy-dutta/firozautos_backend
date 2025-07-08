from rest_framework import viewsets
from .models import*
from .serializers import*
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.response import Response



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


class SupplierPurchaseReturnViewSet(viewsets.ModelViewSet):
    queryset = SupplierPurchaseReturn.objects.all().order_by('-return_date')
    serializer_class = SupplierPurchaseReturnSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        instance = serializer.save()
        purchase_product = instance.purchase_product
        # Update returned_quantity
        purchase_product.returned_quantity += instance.quantity
        purchase_product.save()
        # Update stock
        stock = StockProduct.objects.filter(
            company_name=purchase_product.purchase.company_name,
            part_no=purchase_product.part_no,
            product=purchase_product.product
        ).first()
        if stock:
            stock.current_stock_quantity = max(stock.current_stock_quantity - instance.quantity, 0)
            stock.save()