from django.urls import path
from tables.views import TableListView, ReservationListCreateView, CancelReservationView

urlpatterns = [
    path('', TableListView.as_view(), name='table-list'),
    path('reservations/', ReservationListCreateView.as_view(), name='reservation-list'),
    path('reservations/<int:pk>/cancel/', CancelReservationView.as_view(), name='cancel-reservation'),
]