from rest_framework import serializers
from .models import *

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class ReactSerializer(serializers.ModelSerializer):
    class Meta:
        model = React
        fields = ['employee', 'department']



class SalesDataSerializer(serializers.Serializer):
    month = serializers.CharField(max_length=3)
    sales = serializers.IntegerField()
