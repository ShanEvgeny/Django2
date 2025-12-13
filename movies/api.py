from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from movies.models import Genre, Director, Movie, MovieHall, MovieSession, Ticket
from movies.serializers import GenreSerializer, DirectorSerializer, MovieSerializer, MovieHallSerializer, MovieSessionSerializer, TicketSerializer

class GenresViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
class DirectorsViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
class MoviesViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
class MovieHallsViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = MovieHall.objects.all()
    serializer_class = MovieHallSerializer
class MovieSessionsViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = MovieSession.objects.all()
    serializer_class = MovieSessionSerializer
class TicketsViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer