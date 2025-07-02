from rest_framework import serializers
from .models import*
import json

class ExporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exporter
        fields = '__all__'


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True)

    class Meta:
        model = Employee
        fields = '__all__'

    def to_internal_value(self, data):
        # If education is a JSON string (because it came from multipart), decode it
        if isinstance(data.get('education'), str):
            try:
                data['education'] = json.loads(data['education'])
            except json.JSONDecodeError:
                raise serializers.ValidationError({"education": ["Invalid JSON"]})
        return super().to_internal_value(data)

    def create(self, validated_data):
        education_data = validated_data.pop('education', [])
        employee = Employee.objects.create(**validated_data)
        for edu in education_data:
            Education.objects.create(employee=employee, **edu)
        return employee