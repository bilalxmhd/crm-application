from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = Customer
        fields = '__all__'

    def validate_phone(self,value):
        if not value.isdigit():
            raise serializers.validationError("must contsin only digits")

        if len(value)!=10:
            raise serializers.validationError("must conrain 10 digits") 
        return value   