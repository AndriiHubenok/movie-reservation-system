from django.contrib import admin

from movies.models import Genre, Seat, Movie, Showtime, Hall

admin.site.register(Genre)
admin.site.register(Seat)
admin.site.register(Hall)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    search_fields = ('title',)
    filter_horizontal = ('genres',)

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'start_time', 'price')
    list_filter = ('movie', 'start_time')