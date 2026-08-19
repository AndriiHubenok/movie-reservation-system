from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from movies.models import Movie, Showtime
from movies.permissions import IsAdminOrReadOnly
from movies.serializers import MovieSerializer, ShowtimeSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrReadOnly]

class ShowtimeViewSet(viewsets.ModelViewSet):
    queryset = Showtime.objects.all()
    serializer_class = ShowtimeSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=['get'])
    def available_seats(self, request, pk=None):
        showtime = self.get_object()

        booked_seat_ids = showtime.reservations.filter(
            status__in=['pending', 'confirmed']
        ).values_list('seat_id', flat=True)

        available_seats_qs = showtime.hall.seats.exclude(id__in=booked_seat_ids)

        available_seats_data = [
            {
                "id": seat.id,
                "row": seat.row,
                "number": seat.number
            }
            for seat in available_seats_qs
        ]

        return Response({"available_seats": available_seats_data})
