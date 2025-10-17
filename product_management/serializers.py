
# Serialization <--> Deserialization

from rest_framework import serializers
from product_management.models import Category, Product

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = [
        #     'id', 
        #     'name', 
        #     'slug', 
        #     'description', 
        #     'created_at', 
        #     'updated_at'
        # ]
        fields = '__all__'
        
        
# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'