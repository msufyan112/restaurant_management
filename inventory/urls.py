from django.urls import path
from .views import InventoryListView, RestockItemView, LowStockAlertsView

urlpatterns = [
    path('', InventoryListView.as_view(), name='inventory-list'),
    path('<int:pk>/restock/', RestockItemView.as_view(), name='restock-item'),
    path('alerts/', LowStockAlertsView.as_view(), name='low-stock-alerts'),
]