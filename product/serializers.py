from .models import *
from rest_framework import serializers
from master.serializers import CompanySerializer
from person.models import Supplier
from person.serializers import SupplierSerializer




class ProductCategorySerializer(serializers.ModelSerializer):
    company_detail = CompanySerializer(source='company', read_only=True)

    class Meta:
        model = ProductCategory
        fields = ['id', 'company', 'company_detail', 'category_name']




class ProductSerializer(serializers.ModelSerializer):
    category_detail = ProductCategorySerializer(source='category', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'




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
            'returned_quantity',
        ]




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
        # Optional: handle update of nested, here we'll just update main fields
        instance.supplier = validated_data.get('supplier', instance.supplier)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.purchase_date = validated_data.get('purchase_date', instance.purchase_date)
        instance.invoice_no = validated_data.get('invoice_no', instance.invoice_no)
        instance.total_amount = validated_data.get('total_amount', instance.total_amount)
        instance.discount_amount = validated_data.get('discount_amount', instance.discount_amount)
        instance.total_payable_amount = validated_data.get('total_payable_amount', instance.total_payable_amount)
        instance.save()

        return instance
    




class StockSerializer(serializers.ModelSerializer):
     product = ProductSerializer(read_only=True)
     damage_quantity = serializers.IntegerField(required=False)
     class Meta:
        model = StockProduct
        fields = '__all__'




class SupplierPurchaseReturnSerializer(serializers.ModelSerializer):
    purchase_product = PurchaseProductSerializer(read_only=True)
    purchase_product_id = serializers.PrimaryKeyRelatedField(
        queryset=PurchaseProduct.objects.all(),
        source='purchase_product',
        write_only=True
    )
    class Meta:
        model = SupplierPurchaseReturn
        fields = ['id', 'purchase_product', 'purchase_product_id', 'quantity', 'return_date', 'reason']
        read_only_fields = ['return_date']

    def validate(self, data):
        purchase_product = data['purchase_product']
        quantity = data['quantity']
        if quantity <= 0:
            raise serializers.ValidationError('Return quantity must be positive.')
        if quantity > (purchase_product.purchase_quantity - purchase_product.returned_quantity):
            raise serializers.ValidationError('Cannot return more than purchased minus already returned.')
        return data
