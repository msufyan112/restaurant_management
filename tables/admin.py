from django.contrib import admin
from .models import Table, Reservation

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['number', 'capacity', 'status']
    list_editable = ['status']
    list_filter = ['status']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'table', 'date', 'time', 'guests', 'status']
    list_filter = ['status', 'date']
    search_fields = ['customer_name', 'phone']