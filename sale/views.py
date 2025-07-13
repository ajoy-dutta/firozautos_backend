from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Sale, SaleReturn, SaleProduct, SalePayment
from .serializers import SaleSerializer, SaleReturnSerializer, SalePaymentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from product.models import StockProduct

# Create your views here.

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().order_by('-sale_date')
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def payments(self, request, pk=None):
        """Get all payments for a specific sale"""
        sale = self.get_object()
        payments = sale.payments.all()
        serializer = SalePaymentSerializer(payments, many=True)
        return Response(serializer.data)

class SalePaymentViewSet(viewsets.ModelViewSet):
    queryset = SalePayment.objects.all().order_by('-payment_date')
    serializer_class = SalePaymentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        sale_id = self.request.query_params.get('sale_id')
        if sale_id:
            queryset = queryset.filter(sale_id=sale_id)
        return queryset

    def perform_create(self, serializer):
        """Create a new payment and associate it with the sale"""
        serializer.save()

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
        
        stock = StockProduct.objects.filter(
            company_name=sale_product.sale.company_name,
            part_no=sale_product.part_no,
            product=sale_product.product
        ).first()
        if stock:
            stock.current_stock_quantity += instance.quantity
            stock.save()
