from django.db import models
from menu.models import MenuItem

class InventoryItem(models.Model):
    class Unit(models.TextChoices):
        KG = 'kg', 'Kilogram'
        LITRE = 'litre', 'Litre'
        PIECE = 'piece', 'Piece'

    name = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit = models.CharField(max_length=20, choices=Unit.choices, default=Unit.PIECE)
    low_stock_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    linked_menu_item = models.OneToOneField(
        MenuItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inventory'
    )

    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"