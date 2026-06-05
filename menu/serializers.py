from rest_framework import serializers
from .models import Category, MenuItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = MenuItem
        fields = [
            'id', 'name', 'description', 'price',
            'is_available', 'image_url', 'category', 'category_name'
        ]