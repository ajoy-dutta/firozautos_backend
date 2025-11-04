from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *


# ----------------------------
# Category
# ----------------------------
class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.select_related('company').all()
    serializer_class = ProductCategorySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['category_name', 'company__company_name']
    filterset_fields = ['company']


# ----------------------------
# Bike Model  ✅ NEW
# ----------------------------
class BikeModelViewSet(viewsets.ModelViewSet):
    """
    Supports:
      - GET /bike-models/?company=<id>
      - GET /bike-models/?search=glam
      - POST multipart (company, name, image)
    """
    queryset = BikeModel.objects.select_related('company').all()
    serializer_class = BikeModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'company__company_name']
    filterset_fields = ['company']


# ----------------------------
# Product
# ----------------------------
class ProductViewSet(viewsets.ModelViewSet):
    """
    Useful query params:
      - ?company=<id>
      - ?category=<id>
      - ?bike_model=<id>
      - ?model_no=Glamour          (legacy text filter)
      - ?search=clutch             (name/part/brand search)
    """
    queryset = (
        Product.objects
        .select_related('company', 'category', 'bike_model')
        .all()
    )
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    # broad but practical search fields for admin + shop
    search_fields = [
        'product_name',
        'part_no',
        'brand_name',
        'model_no',
        'description',
    ]
    filterset_fields = ['company', 'category', 'bike_model', 'model_no']

    def get_queryset(self):
        qs = super().get_queryset()

        # extra explicit filters (helpful when not using filterset on FE)
        company = self.request.query_params.get('company')
        if company:
            qs = qs.filter(company_id=company)

        bike_model = self.request.query_params.get('bike_model')
        if bike_model:
            qs = qs.filter(bike_model_id=bike_model)

        model_no = self.request.query_params.get('model_no')
        if model_no:
            qs = qs.filter(model_no__iexact=model_no)

        brand_name = self.request.query_params.get('brand_name')
        if brand_name:
            qs = qs.filter(brand_name__iexact=brand_name)

        return qs


# ----------------------------
# Supplier Purchase
# ----------------------------
class SupplierPurchaseViewSet(viewsets.ModelViewSet):
    queryset = SupplierPurchase.objects.all().order_by('-purchase_date')
    serializer_class = SupplierPurchaseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ----------------------------
# Stock
# ----------------------------
class StockViewSet(viewsets.ModelViewSet):
    queryset = StockProduct.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['part_no', 'product__product_name', 'company_name']
    filterset_fields = ['product', 'company_name']


# ----------------------------
# Supplier Purchase Return
# ----------------------------
class SupplierPurchaseReturnViewSet(viewsets.ModelViewSet):
    queryset = SupplierPurchaseReturn.objects.all().order_by('-return_date')
    serializer_class = SupplierPurchaseReturnSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        invoice_no = self.request.query_params.get('invoice_no')
        if invoice_no:
            queryset = queryset.filter(purchase_product__purchase__invoice_no=invoice_no)
        return queryset

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


# ----------------------------
# Order
# ----------------------------
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
