from django.shortcuts import render
from rest_framework import viewsets

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
