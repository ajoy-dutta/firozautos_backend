from rest_framework import serializers
from .models import*


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
    
    def create(self, validated_data):
        education_data = validated_data.pop('education', [])
        employee = Employee.objects.create(**validated_data)
        for edu in education_data:
            Education.objects.create(employee=employee, **edu)
        return employee

    def update(self, instance, validated_data):
        education_data = validated_data.pop('education', [])

        # Update all fields of Employee
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or add education records
        for edu_data in education_data:
            edu_id = edu_data.get('id', None)

            if edu_id:
                # Update existing if ID is given
                try:
                    edu_instance = Education.objects.get(id=edu_id, employee=instance)
                    for attr, value in edu_data.items():
                        setattr(edu_instance, attr, value)
                    edu_instance.save()
                except Education.DoesNotExist:
                    # If not found, create new
                    Education.objects.create(employee=instance, **edu_data)
            else:
                # Create new entry if ID not provided
                Education.objects.create(employee=instance, **edu_data)

        return instance
    





class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

