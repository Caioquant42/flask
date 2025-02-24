from rest_framework import serializers
from .models import *

class BRStockRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BRStockRecommendation
        fields = '__all__'

class USAStockRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = USAStockRecommendation
        fields = '__all__'