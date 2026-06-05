from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        STAFF = 'staff', 'Staff'
        CUSTOMER = 'customer', 'Customer'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='restaurant_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='restaurant_user_permissions_set',
        blank=True
    )

    def is_admin_or_staff(self):
        return self.role in [self.Role.ADMIN, self.Role.STAFF]

    def __str__(self):
        return f"{self.username} ({self.role})"