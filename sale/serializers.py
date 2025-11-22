from rest_framework import serializers
from .models import Sale, SaleProduct, SalePayment, SaleReturn
from person.models import Customer
from person.serializers import CustomerSerializer
from product.models import Product, StockProduct
from product.serializers import ProductSerializer
from master.models import PaymentMode, BankMaster
from master.serializers import PaymentModeSerializer, BankMasterSerializer
from django.db import transaction

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

    def validate(self, data):
        sale_quantity = data.get('sale_quantity')
        product = data.get('product')
        part_no = data.get('part_no')

        stock = StockProduct.objects.filter(product=product, part_no=part_no).first()

        if not stock:
          raise serializers.ValidationError(f"No stock record found for {product} ({part_no}).")

        if stock.current_stock_quantity < sale_quantity:
            raise serializers.ValidationError(
                f"Insufficient stock! Only {stock.current_stock_quantity} available."
            )
        
        return data

       



class SalePaymentSerializer(serializers.ModelSerializer):
    bank_name = BankMasterSerializer(read_only=True)
    bank_name_id = serializers.PrimaryKeyRelatedField(
        queryset=BankMaster.objects.all(),
        source='bank_name',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = SalePayment
        fields = [
            'id',
            'payment_mode',
            'bank_name',
            'bank_name_id',
            'account_no',
            'cheque_no',
            'paid_amount',
            'remarks',
            'payment_date',
        ]
        read_only_fields = ['payment_date']

    def validate(self, data):
        payment_mode = data.get('payment_mode')
        bank_name = data.get('bank_name')
        account_no = data.get('account_no')
        cheque_no = data.get('cheque_no')
        
        # If payment mode requires bank details, validate them
        if payment_mode and payment_mode.lower() in ['bank transfer', 'cheque', 'online']:
            if not bank_name:
                raise serializers.ValidationError("Bank name is required for this payment mode.")
            if not account_no:
                raise serializers.ValidationError("Account number is required for this payment mode.")
        
        # If cheque payment, validate cheque number
        if payment_mode and payment_mode.lower() == 'cheque':
            if not cheque_no:
                raise serializers.ValidationError("Cheque number is required for cheque payments.")
        
        return data



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
            'sale_date',
            'invoice_no',
            'total_amount',
            'discount_amount',
            'total_payable_amount',
            'products',
            'payments',
            'created_at',
        ]
        read_only_fields = ['invoice_no', 'created_at']

    @transaction.atomic
    def create(self, validated_data):
        products_data = validated_data.pop('products', [])
        payments_data = validated_data.pop('payments', [])
        sale = Sale.objects.create(**validated_data)

        # Create SaleProduct records
        for product_data in products_data:
            SaleProduct.objects.create(sale=sale, **product_data)

        # Create SalePayment records
        for payment_data in payments_data:
            SalePayment.objects.create(sale=sale, **payment_data)

        return sale




class SaleReturnSerializer(serializers.ModelSerializer):
    sale_product = SaleProductSerializer(read_only=True)
    sale_product_id = serializers.PrimaryKeyRelatedField(
        queryset=SaleProduct.objects.all(),
        source='sale_product',
        write_only=True
    )
    class Meta:
        model = SaleReturn
        fields = ['id', 'sale_product', 'sale_product_id', 'quantity', 'return_date']
        read_only_fields = ['return_date']

    def validate(self, data):
        sale_product = data['sale_product']
        quantity = data['quantity']
        if quantity <= 0:
            raise serializers.ValidationError('Return quantity must be positive.')
        if quantity > (sale_product.sale_quantity - sale_product.returned_quantity):
            raise serializers.ValidationError('Cannot return more than sold minus already returned.')
        return data 