from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Table, Reservation
from .serializers import TableSerializer, ReservationSerializer

class TableListView(generics.ListCreateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CancelReservationView(generics.UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        reservation = self.get_object()

        if reservation.status == 'cancelled':
            return Response(
                {"detail": "Reservation is already cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Free up the table
        reservation.table.status = 'available'
        reservation.table.save()

        reservation.status = 'cancelled'
        reservation.save()

        return Response(
            {"detail": "Reservation cancelled successfully."},
            status=status.HTTP_200_OK
        )