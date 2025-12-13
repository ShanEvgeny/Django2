from django.contrib import admin

from movies.models import Genre, Director, Movie, MovieHall, MovieSession, Ticket

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','description']
@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name','date_of_birth']
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','description','movie_running_time']
    filter_horizontal = ['directors','genres']
@admin.register(MovieHall)
class MovieHallAdmin(admin.ModelAdmin):
    list_display = ['id', 'sequence_number','sequence_number','count_of_seats']
@admin.register(MovieSession)
class MovieSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie_hall','movie','date_of_event']
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie_session','count_of_seats_purchased']