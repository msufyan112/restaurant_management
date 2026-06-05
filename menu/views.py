from rest_framework import generics, permissions
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer

class IsAdminOrStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin_or_staff()

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrStaffOrReadOnly]

class MenuItemListCreateView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrStaffOrReadOnly]

    def get_queryset(self):
        queryset = MenuItem.objects.all()
        # Filter by category if provided: /api/menu/items/?category=1
        category = self.request.query_params.get('category')
        available = self.request.query_params.get('available')
        if category:
            queryset = queryset.filter(category=category)
        if available:
            queryset = queryset.filter(is_available=True)
        return queryset

class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrStaffOrReadOnly]