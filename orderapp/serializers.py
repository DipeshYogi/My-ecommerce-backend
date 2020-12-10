from rest_framework import serializers
from .models import ECH

class OrderSerializer(serializers.Serializer):
  """Order Serializer"""
  HCUST = serializers.IntegerField(required=True)
  HSHOP = serializers.IntegerField(required=True)
  HPROD = serializers.JSONField(required=True)


# class OrderInfoSerializer(serializers.Serializer):
#   """Order info"""
#   HORD = serializers.IntegerField(required=True)
#   HCUST = serializers.IntegerField(required=True)
#   HSHOP = serializers.IntegerField(required=True)
#   HSNME = serializers.CharField(required=True)
#   HEDTE = serializers.DateField(required=True)
#   HSTS = serializers.CharField(required=True)


# class OrderLineSerializer(serializers.Serializer):
#   """Order line details serializer"""
#   LORD = serializers.IntegerField(required=True)
#   LLINE = serializers.IntegerField(required=True)
#   LPROD = serializers.CharField(required=True)
#   LQORD = serializers.IntegerField(required=True)
#   LPRIC = serializers.IntegerField(required=True)
#   LDISC = serializers.IntegerField(required=True)

    
