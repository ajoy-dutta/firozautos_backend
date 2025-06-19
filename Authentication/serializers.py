from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import*

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'full_name', 'phone',
            'password', 'confirm_password', 'profile_picture'
        ]
        extra_kwargs = {'password':{'write_only':True}}
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            return serializers.ValidationError("Password do not match.")
        return data
    
    def create(self,validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
