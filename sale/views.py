from django.shortcuts import render
from rest_framework import viewsets
from .models import Sale, SaleReturn, SaleProduct
from .serializers import SaleSerializer, SaleReturnSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().order_by('-sale_date')
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class SaleReturnViewSet(viewsets.ModelViewSet):
    queryset = SaleReturn.objects.all().order_by('-return_date')
    serializer_class = SaleReturnSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        invoice_no = self.request.query_params.get('invoice_no')
        if invoice_no:
            queryset = queryset.filter(sale_product__sale__invoice_no=invoice_no)
        return queryset

    def perform_create(self, serializer):
        instance = serializer.save()
        sale_product = instance.sale_product
        sale_product.returned_quantity += instance.quantity
        sale_product.save()
        # Update stock: increase current_stock_quantity
        from product.models import StockProduct
        stock = StockProduct.objects.filter(
            company_name=sale_product.sale.company_name,
            part_no=sale_product.part_no,
            product=sale_product.product
        ).first()
        if stock:
            stock.current_stock_quantity += instance.quantity
            stock.save()
