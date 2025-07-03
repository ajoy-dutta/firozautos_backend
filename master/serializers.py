from rest_framework import serializers
from .models import*




class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'



class CostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CostCategory
        fields = '__all__'


class SourceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceCategory
        fields = '__all__'


class PaymentModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMode
        fields = '__all__'


class DistrictMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistrictMaster
        fields = '__all__'


class CountryMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryMaster
        fields = '__all__'


class SupplierTypeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierTypeMaster
        fields = '__all__'


class BankCategoryMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankCategoryMaster
        fields = '__all__'
        

class BankMasterSerializer(serializers.ModelSerializer):
    bank_category_detail = BankCategoryMasterSerializer(source='bank_category', read_only=True)

    class Meta:
        model = BankMaster
        fields = '__all__'
