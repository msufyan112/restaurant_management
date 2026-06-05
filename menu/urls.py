from django.urls import path
from .views import CategoryListCreateView, MenuItemListCreateView, MenuItemDetailView

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('items/', MenuItemListCreateView.as_view(), name='menu-list'),
    path('items/<int:pk>/', MenuItemDetailView.as_view(), name='menu-detail'),
]