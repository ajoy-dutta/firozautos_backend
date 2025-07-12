from rest_framework import serializers
from .models import Sale, SaleProduct, SalePayment, SaleReturn
from person.models import Customer
from person.serializers import CustomerSerializer
from product.models import Product
from product.serializers import ProductSerializer

class SaleProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = SaleProduct
        fields = [
            'id',
            'product',
            'product_id',
            'part_no',
            'sale_quantity',
            'sale_price',
            'percentage',
            'sale_price_with_percentage',
            'total_price',
        ]

class SalePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalePayment
        fields = [
            'id',
            'payment_mode',
            'bank_name',
            'account_no',
            'cheque_no',
            'paid_amount',
            'remarks',
        ]

class SaleSerializer(serializers.ModelSerializer):
    products = SaleProductSerializer(many=True)
    payments = SalePaymentSerializer(many=True)
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source='customer',
        write_only=True
    )

    class Meta:
        model = Sale
        fields = [
            'id',
            'customer',
            'customer_id',
            'company_name',
            'sale_date',
            'invoice_no',
            'total_amount',
            'discount_amount',
            'total_payable_amount',
            'products',
            'payments',
            'created_at',
        ]
        read_only_fields = ['created_at']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        payments_data = validated_data.pop('payments')
        sale = Sale.objects.create(**validated_data)
        for product in products_data:
            SaleProduct.objects.create(sale=sale, **product)
        for payment in payments_data:
            SalePayment.objects.create(sale=sale, **payment)
        return sale

    def update(self, instance, validated_data):
        instance.customer = validated_data.get('customer', instance.customer)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.sale_date = validated_data.get('sale_date', instance.sale_date)
        instance.invoice_no = validated_data.get('invoice_no', instance.invoice_no)
        instance.total_amount = validated_data.get('total_amount', instance.total_amount)
        instance.discount_amount = validated_data.get('discount_amount', instance.discount_amount)
        instance.total_payable_amount = validated_data.get('total_payable_amount', instance.total_payable_amount)
        instance.save()
        return instance 

class SaleReturnSerializer(serializers.ModelSerializer):
    sale_product = SaleProductSerializer(read_only=True)
    sale_product_id = serializers.PrimaryKeyRelatedField(
        queryset=SaleProduct.objects.all(),
        source='sale_product',
        write_only=True
    )
    class Meta:
        model = SaleReturn
        fields = ['id', 'sale_product', 'sale_product_id', 'quantity', 'return_date', 'reason']
        read_only_fields = ['return_date']

    def validate(self, data):
        sale_product = data['sale_product']
        quantity = data['quantity']
        if quantity <= 0:
            raise serializers.ValidationError('Return quantity must be positive.')
        if quantity > (sale_product.sale_quantity - sale_product.returned_quantity):
            raise serializers.ValidationError('Cannot return more than sold minus already returned.')
        return data 