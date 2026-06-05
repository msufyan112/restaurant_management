from rest_framework import serializers
from .models import Table, Reservation

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'number', 'capacity', 'status']

class ReservationSerializer(serializers.ModelSerializer):
    table_number = serializers.IntegerField(source='table.number', read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id', 'table', 'table_number', 'customer_name',
            'phone', 'guests', 'date', 'time', 'status', 'created_at'
        ]
        read_only_fields = ['status', 'created_at']

    def validate(self, attrs):
        table = attrs['table']
        guests = attrs['guests']

        if table.status != 'available':
            raise serializers.ValidationError("This table is not available.")

        if guests > table.capacity:
            raise serializers.ValidationError(
                f"Table capacity is {table.capacity} but you requested {guests} guests."
            )
        return attrs

    def create(self, validated_data):
        table = validated_data['table']
        table.status = 'reserved'
        table.save()
        return super().create(validated_data)