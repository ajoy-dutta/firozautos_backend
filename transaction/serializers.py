from rest_framework import serializers
from .models import *


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'



class PurchaseEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseEntry
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'



class IncomeSrializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'



class CombinedPurchaseSerializer(serializers.Serializer):
    date = serializers.DateField()
    invoice_no = serializers.CharField()
    part_no = serializers.CharField()
    product_name = serializers.CharField()
    supplier_or_exporter = serializers.CharField()
    quantity = serializers.IntegerField()
    purchase_amount = serializers.DecimalField(max_digits=12, decimal_places=2)