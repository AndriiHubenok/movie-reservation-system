from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    # Для ImageField потрібна додаткова бібліотека (Pillow), тому для простоти використаємо URL
    poster = models.URLField(blank=True, null=True)

    genres = models.ManyToManyField(Genre, related_name='movies')

    def __str__(self):
        return self.title

class Showtime(models.Model):

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.movie.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

class Seat(models.Model):
    row = models.CharField(max_length=10)
    number = models.IntegerField()

    class Meta:
        unique_together = ('row', 'number')

    def __str__(self):
        return f"Row {self.row}, Seat {self.number}"