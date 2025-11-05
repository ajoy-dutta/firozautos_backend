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