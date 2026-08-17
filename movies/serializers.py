from rest_framework import serializers

from movies.models import Genre, Movie, Showtime

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class MovieSerializer(serializers.ModelSerializer):

    genres = GenreSerializer(many=True, read_only=True)

    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), source='genres', write_only=True, many=True
    )

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'poster', 'genres', 'genre_ids']

class ShowtimeSerializer(serializers.ModelSerializer):

    movie_title = serializers.CharField(source='movie.title', read_only=True)

    class Meta:
        model = Showtime
        fields = ['id', 'movie', 'movie_title', 'start_time', 'end_time', 'price']