from rest_framework import serializers
from .models import Addresses


class AddressSerializer(serializers.Serializer):
    """Serializer for user delivery address"""
    id = serializers.IntegerField(required=False)
    address1 = serializers.CharField(max_length=50, required=True)
    address2 = serializers.CharField(max_length=50, required=False)
    pincode = serializers.CharField(max_length=8, required=True)
    phone = serializers.CharField(max_length=12, required=True)
    is_active =serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        addr = Addresses.objects.create(**validated_data)
        
        return addr
    
    def update(self, instance, validated_data):
        instance.address1 = validated_data.get('address1', instance.address1)
        instance.address2 = validated_data.get('address2', instance.address2)
        instance.pincode = validated_data.get('pincode', instance.pincode)
        instance.phone = validated_data.get('phone', instance.phone)

        instance.save()
        return instance

