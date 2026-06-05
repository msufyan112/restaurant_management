from django.db import models
from menu.models import MenuItem
from tables.models import Table

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PREPARING = 'preparing', 'Preparing'
        SERVED = 'served', 'Served'
        PAID = 'paid', 'Paid'
        CANCELLED = 'cancelled', 'Cancelled'

    table = models.ForeignKey(
        Table,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total(self):
        total = sum(item.subtotal() for item in self.order_items.all())
        self.total_price = total
        self.save()

    def __str__(self):
        return f"Order #{self.id} - Table {self.table.number} ({self.status})"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def subtotal(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"