from django.db import models

class Table(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        OCCUPIED = 'occupied', 'Occupied'
        RESERVED = 'reserved', 'Reserved'

    number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE
    )

    def __str__(self):
        return f"Table {self.number} ({self.status})"

class Reservation(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'
        COMPLETED = 'completed', 'Completed'

    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    customer_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    guests = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CONFIRMED
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - Table {self.table.number} on {self.date}"