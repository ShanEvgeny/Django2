from django.contrib import admin

from movies.models import Genre, MovieHouse, Director, Movie, MovieHall, MovieSession, Ticket

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','description']
@admin.register(MovieHouse)
class MovieHouseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','address','phone_number']
@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name','date_of_birth']
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','description','movie_running_time']
    filter_horizontal = ['directors','genres']
    pass
@admin.register(MovieHall)
class MovieHallAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie_house','sequence_number','sequence_number','count_of_seats']
    pass
@admin.register(MovieSession)
class MovieSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie_hall','movie','date_of_event']
    pass
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie_session','count_of_seats_purchased']
    pass