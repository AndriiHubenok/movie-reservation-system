from django.db.models import Sum, Count, Q
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import Movie, Showtime
from movies.permissions import IsAdminOrReadOnly
from movies.serializers import MovieSerializer, ShowtimeSerializer
from reservations.models import Reservation


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        genre_id = self.request.query_params.get('genre_id')
        if genre_id:
            queryset = queryset.filter(genres__id=genre_id)
        return queryset

class ShowtimeViewSet(viewsets.ModelViewSet):
    queryset = Showtime.objects.all()
    serializer_class = ShowtimeSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(start_time__date=date)

        return queryset

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

class AdminReportView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_stats = Reservation.objects.filter(status='confirmed').aggregate(
            total_revenue=Sum('showtime__price'),
            total_tickets=Count('id')
        )

        movies_report = Movie.objects.annotate(
            sold_tickets=Count(
                'showtimes__reservations',
                filter=Q(showtimes__reservations__status='pending')
            ),
            movie_revenue=Sum(
                'showtimes__reservations__showtime__price',
                filter=Q(showtimes__reservations__status='pending')
            )
        ).order_by('-movie_revenue')

        report_data = {
            "overall": {
                "revenue": total_stats['total_revenue'] or 0,
                "tickets_sold": total_stats['total_tickets']
            },
            "by_movie": [
                {
                    "title": movie.title,
                    "tickets_sold": movie.sold_tickets,
                    "revenue": movie.movie_revenue or 0
                }
                for movie in movies_report
            ]
        }

        return Response(report_data)
