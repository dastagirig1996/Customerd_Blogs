from rest_framework import serializers
from .models import Customer,RefreshToken
from datetime import date

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def validate_first_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("First name must be contain alphabets only")
        return value
 
    def validate_last_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Last name must be contain alphabets only.")
        return value
 
    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must be contain only digits.")
        if len(value) < 10 or len(value) > 10:
            raise serializers.ValidationError("Phone number must be 10 digits long.")
        return value
 
    def validate_date_of_birth(self, value):
        if value >= date.today():
            raise serializers.ValidationError("Please enter your correct date of birth")
        return value


