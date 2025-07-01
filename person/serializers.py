from rest_framework import serializers
from .models import*
import json
from master.serializers import *
from master.models import *

class ExporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exporter
        fields = '__all__'


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True, required=False)

    class Meta:
        model = Employee
        fields = '__all__'

    def create(self, validated_data):
        education_data = validated_data.pop('education', [])
        employee = Employee.objects.create(**validated_data)
        for edu in education_data:
            Education.objects.create(employee=employee, **edu)
        return employee

    def update(self, instance, validated_data):
        education_data = validated_data.pop('education', None)

        # Update main fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle education records
        if education_data is not None:
            # Replace all existing records
            instance.education.all().delete()
            for edu in education_data:
                Education.objects.create(employee=instance, **edu)

        return instance
    

class SupplierSerializer(serializers.ModelSerializer):
    supplier_type_detail = SupplierTypeMasterSerializer(source='supplier_type', read_only=True)
    district_detail = DistrictMasterSerializer(source='district', read_only=True)

    class Meta:
        model = Supplier
        fields = '__all__'


