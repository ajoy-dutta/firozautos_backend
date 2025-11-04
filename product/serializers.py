from .models import *
from rest_framework import serializers
from master.serializers import CompanySerializer
from person.models import Supplier
from person.serializers import SupplierSerializer


# ----------------------------
# Category Serializer
# ----------------------------
class ProductCategorySerializer(serializers.ModelSerializer):
    company_detail = CompanySerializer(source='company', read_only=True)

    class Meta:
        model = ProductCategory
        fields = ['id', 'company', 'company_detail', 'category_name']


# ----------------------------
# Bike Model Serializer
# ----------------------------
class BikeModelSerializer(serializers.ModelSerializer):
    company_detail = CompanySerializer(source="company", read_only=True)

    class Meta:
        model = BikeModel
        fields = ["id", "company", "company_detail", "name", "image", "slug"]


# ----------------------------
# Product Serializer
# ----------------------------
class ProductSerializer(serializers.ModelSerializer):
    category_detail = ProductCategorySerializer(source='category', read_only=True)
    company_detail = CompanySerializer(source='company', read_only=True)
    bike_model_detail = BikeModelSerializer(source="bike_model", read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


# ----------------------------
# Purchase Product Serializer
# ----------------------------
class PurchaseProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = PurchaseProduct
        fields = [
            'id',
            'product',
            'product_id',
            'part_no',
            'purchase_quantity',
            'purchase_price',
            'percentage',
            'purchase_price_with_percentage',
            'total_price',
        ]


# ----------------------------
# Purchase Payment Serializer
# ----------------------------
class PurchasePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasePayment
        fields = [
            'id',
            'payment_mode',
            'bank_name',
            'account_no',
            'cheque_no',
            'paid_amount',
        ]


# ----------------------------
# Supplier Purchase Serializer
# ----------------------------
class SupplierPurchaseSerializer(serializers.ModelSerializer):
    products = PurchaseProductSerializer(many=True)
    payments = PurchasePaymentSerializer(many=True)
    supplier = SupplierSerializer(read_only=True)
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),
        source='supplier',
        write_only=True
    )
    total_returned_quantity = serializers.IntegerField(read_only=True)
    total_returned_value = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = SupplierPurchase
        fields = [
            'id',
            'supplier',
            'supplier_id',
            'company_name',
            'purchase_date',
            'invoice_no',
            'total_amount',
            'discount_amount',
            'total_payable_amount',
            'products',
            'payments',
            'created_at',
            'total_returned_quantity',
            'total_returned_value',
        ]
        read_only_fields = ['created_at']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        payments_data = validated_data.pop('payments')
        purchase = SupplierPurchase.objects.create(**validated_data)

        for product in products_data:
            PurchaseProduct.objects.create(purchase=purchase, **product)

        for payment in payments_data:
            PurchasePayment.objects.create(purchase=purchase, **payment)

        return purchase

    def update(self, instance, validated_data):
        instance.supplier = validated_data.get('supplier', instance.supplier)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.purchase_date = validated_data.get('purchase_date', instance.purchase_date)
        instance.invoice_no = validated_data.get('invoice_no', instance.invoice_no)
        instance.total_amount = validated_data.get('total_amount', instance.total_amount)
        instance.discount_amount = validated_data.get('discount_amount', instance.discount_amount)
        instance.total_payable_amount = validated_data.get('total_payable_amount', instance.total_payable_amount)
        instance.save()
        return instance


# ----------------------------
# Stock Serializer
# ----------------------------
class StockSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = StockProduct
        fields = '__all__'


# ----------------------------
# Supplier Purchase Return Serializer
# ----------------------------
class SupplierPurchaseReturnSerializer(serializers.ModelSerializer):
    purchase_product = PurchaseProductSerializer(read_only=True)
    purchase_product_id = serializers.PrimaryKeyRelatedField(
        queryset=PurchaseProduct.objects.all(),
        source='purchase_product',
        write_only=True
    )

    class Meta:
        model = SupplierPurchaseReturn
        fields = ['id', 'purchase_product', 'purchase_product_id', 'quantity', 'return_date']
        read_only_fields = ['return_date']

    def validate(self, data):
        purchase_product = data['purchase_product']
        quantity = data['quantity']
        if quantity <= 0:
            raise serializers.ValidationError('Return quantity must be positive.')
        if quantity > (purchase_product.purchase_quantity - purchase_product.returned_quantity):
            raise serializers.ValidationError('Cannot return more than purchased minus already returned.')
        return data


# ----------------------------
# Order Item Serializer
# ----------------------------
class OrderItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product')

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product_id',
            'quantity',
            'order_price',
            'product_details',
        ]


# ----------------------------
# Order Serializer
# ----------------------------
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'order_no', 'order_date', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        instance.order_no = validated_data.get('order_no', instance.order_no)
        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.save()

        existing_item_ids = [item.id for item in instance.items.all()]
        new_item_ids = []

        for item_data in items_data:
            item_id = item_data.get('id', None)
            if item_id and item_id in existing_item_ids:
                item = OrderItem.objects.get(id=item_id, order=instance)
                for attr, value in item_data.items():
                    setattr(item, attr, value)
                item.save()
                new_item_ids.append(item_id)
            else:
                item = OrderItem.objects.create(order=instance, **item_data)
                new_item_ids.append(item.id)

        for item in instance.items.all():
            if item.id not in new_item_ids:
                item.delete()

        return instance
