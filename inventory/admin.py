from django.contrib import admin
from .models import InventoryItem

@admin.register(InventoryItem)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'unit', 'low_stock_threshold', 'is_low_stock']
    list_filter = ['unit']
    search_fields = ['name']

    def is_low_stock(self, obj):
        return obj.is_low_stock()
    is_low_stock.boolean = True