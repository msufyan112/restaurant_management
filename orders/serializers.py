from rest_framework import serializers
from .models import Order, OrderItem
from menu.models import MenuItem

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_name', 'quantity', 'unit_price', 'subtotal']
        read_only_fields = ['unit_price']

    def get_subtotal(self, obj):
        return obj.subtotal()

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'table', 'status', 'total_price', 'order_items', 'created_at']
        read_only_fields = ['status', 'total_price', 'created_at']

    def validate_order_items(self, items):
        if not items:
            raise serializers.ValidationError("Order must have at least one item.")
        return items

    def create(self, validated_data):
        items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            menu_item = item_data['menu_item']

            # Check availability
            if not menu_item.is_available:
                raise serializers.ValidationError(f"{menu_item.name} is not available.")

            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=item_data['quantity'],
                unit_price=menu_item.price
            )

            # Auto-decrement inventory if linked
            if hasattr(menu_item, 'inventory'):
                inv = menu_item.inventory
                inv.quantity -= item_data['quantity']
                if inv.quantity < 0:
                    inv.quantity = 0
                inv.save()

                # Mark menu item unavailable if out of stock
                if inv.quantity == 0:
                    menu_item.is_available = False
                    menu_item.save()

        order.calculate_total()
        return order

class UpdateOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']