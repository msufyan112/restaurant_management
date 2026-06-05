from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import InventoryItem
from .serializers import InventoryItemSerializer, RestockSerializer

class IsAdminOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin_or_staff()

class InventoryListView(generics.ListCreateAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAdminOrStaff]

class RestockItemView(APIView):
    permission_classes = [IsAdminOrStaff]

    def patch(self, request, pk):
        try:
            item = InventoryItem.objects.get(pk=pk)
        except InventoryItem.DoesNotExist:
            return Response({"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = RestockSerializer(data=request.data)
        if serializer.is_valid():
            item.quantity += serializer.validated_data['quantity']
            item.save()

            # Re-enable menu item if it was disabled due to stock
            if item.linked_menu_item and not item.linked_menu_item.is_available:
                item.linked_menu_item.is_available = True
                item.linked_menu_item.save()

            return Response(InventoryItemSerializer(item).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LowStockAlertsView(APIView):
    permission_classes = [IsAdminOrStaff]

    def get(self, request):
        low_stock = InventoryItem.objects.all()
        alerts = [item for item in low_stock if item.is_low_stock()]
        serializer = InventoryItemSerializer(alerts, many=True)
        return Response(serializer.data)