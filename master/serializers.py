from rest_framework import serializers
from .models import*

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

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