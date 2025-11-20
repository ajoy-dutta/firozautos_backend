from rest_framework import serializers



class CombinedPurchaseSerializer(serializers.Serializer):
    date = serializers.DateField()
    invoice_no = serializers.CharField()
    part_no = serializers.CharField()
    product_name = serializers.CharField()
    supplier_or_exporter = serializers.CharField()
    quantity = serializers.IntegerField()
    purchase_amount = serializers.DecimalField(max_digits=12, decimal_places=2)



class CombinedExpenseSerializer(serializers.Serializer):
    date = serializers.DateField()
    voucher_no = serializers.CharField()
    account_title = serializers.CharField()
    cost_category = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    description = serializers.CharField()
    transaction_type = serializers.CharField()

