from rest_framework import serializers
from .models import InventoryItem

class InventoryItemSerializer(serializers.ModelSerializer):
    is_low_stock = serializers.SerializerMethodField()

    class Meta:
        model = InventoryItem
        fields = [
            'id', 'name', 'quantity', 'unit',
            'low_stock_threshold', 'is_low_stock', 'linked_menu_item'
        ]

    def get_is_low_stock(self, obj):
        return obj.is_low_stock()

class RestockSerializer(serializers.Serializer):
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value