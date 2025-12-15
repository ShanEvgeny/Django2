from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker
import datetime
from django.utils.dateparse import parse_duration

from movies.models import Genre, Director, Movie, MovieHall, MovieSession, Ticket

class GenresViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        genre = baker.make("Genre")
        r = self.client.get('/api/genres/')
        data = r.json()
        print(data)
        assert genre.id == data[0]['id']
        assert genre.title == data[0]['title']
        assert genre.description == data[0]['description']

    def test_create(self):
        r = self.client.post("/api/genres/",{
            'title': "Жанр",
            'description': "Описание"
        })
        new_genre_id = r.json()['id']
        genres = Genre.objects.all()
        assert len(genres) == 1
        new_genre = Genre.objects.filter(id = new_genre_id).first()
        assert new_genre.title == "Жанр"
        assert new_genre.description == "Описание"

    def test_delete(self):
        genres = baker.make("Genre",10)
        r = self.client.get('/api/genres/')
        data = r.json()
        assert len(data) == 10
        genre_id_to_delete = genres[3].id
        self.client.delete(f'/api/genres/{genre_id_to_delete}/')
        r = self.client.get('/api/genres/')
        data = r.json()
        assert len(data) == 9
        assert genre_id_to_delete not in [i['id'] for i in data]

    def test_update(self):
        genres = baker.make("Genre",10)
        genre: Genre = genres[2]
        r = self.client.get(f'/api/genres/{genre.id}/')
        data = r.json()
        assert data['title'] == genre.title
        r = self.client.put(f'/api/genres/{genre.id}/',{
            'title': 'Жанр'
        })
        assert r.status_code == 200
        r = self.client.get(f'/api/genres/{genre.id}/')
        data = r.json()
        assert data['title'] == "Жанр"
        genre.refresh_from_db()
        assert data['title'] == genre.title

class DirectorsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        director = baker.make("movies.Director",date_of_birth = '2025-12-15')
        r = self.client.get('/api/directors/')
        data = r.json()
        print(data)
        assert director.id == data[0]['id']
        assert director.full_name == data[0]['full_name']
        assert director.date_of_birth == data[0]['date_of_birth']

    def test_create(self):
        r = self.client.post("/api/directors/",{
            'full_name': "Режиссер",
            'date_of_birth': "1995-12-15"
        })
        new_drctr_id = r.json()['id']
        drctrs = Director.objects.all()
        assert len(drctrs) == 1
        new_drctr = Director.objects.filter(id = new_drctr_id).first()
        assert new_drctr.full_name == "Режиссер"
        assert str(new_drctr.date_of_birth) == "1995-12-15"

    def test_delete(self):
        directors = baker.make("Director",10)
        r = self.client.get('/api/directors/')
        data = r.json()
        assert len(data) == 10
        director_id_to_delete = directors[3].id
        self.client.delete(f'/api/directors/{director_id_to_delete}/')
        r = self.client.get('/api/directors/')
        data = r.json()
        assert len(data) == 9
        assert director_id_to_delete not in [i['id'] for i in data]

    def test_update(self):
        directors = baker.make("Director", 10)
        director: Director = directors[2]
        r = self.client.get(f'/api/directors/{director.id}/')
        data = r.json()
        assert data['full_name'] == director.full_name
        r = self.client.patch(f'/api/directors/{director.id}/',{
            'full_name': 'Режиссер'
        })
        assert r.status_code == 200
        r = self.client.get(f'/api/directors/{director.id}/')
        data = r.json()
        assert data['full_name'] == "Режиссер"
        director.refresh_from_db()
        assert data['full_name'] == director.full_name

class MoviesViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        director1 = baker.make("movies.Director",date_of_birth = '2025-12-15')
        director2 = baker.make("movies.Director",date_of_birth = '2025-12-14')
        genre1 = baker.make("Genre")
        genre2 = baker.make("Genre")
        movie = baker.make("Movie", movie_running_time = datetime.timedelta(minutes=30))
        movie.directors.add(director1, director2)
        movie.genres.add(genre1, genre2)
        r = self.client.get('/api/movies/')
        data = r.json()
        print(data)
        assert movie.id == data[0]['id']
        assert movie.title == data[0]['title']
        assert movie.movie_running_time == parse_duration(data[0]['movie_running_time'])
        assert movie.directors.count() == 2
        assert movie.genres.count() == 2
        directors_list_id = list(movie.directors.values_list('id', flat=True))
        genres_list_id = list(movie.genres.values_list('id', flat=True))
        assert directors_list_id == data[0]['directors']
        assert genres_list_id == data[0]['genres']

    def test_create(self):
        director1 = baker.make("movies.Director",date_of_birth = '2025-12-15')
        director2 = baker.make("movies.Director",date_of_birth = '2025-12-14')
        genre1 = baker.make("Genre")
        genre2 = baker.make("Genre")
        directors = [director1.id,director2.id]
        genres = [genre1.id,genre2.id]
        r = self.client.post("/api/movies/",{
            'title': "Кино",
            'description': "Описание",
            'movie_running_time': "1:30:00",
            'directors': directors,
            'genres': genres
        })
        new_mv_id = r.json()['id']
        mvs = Movie.objects.all()
        assert len(mvs) == 1
        new_mv = Movie.objects.filter(id = new_mv_id).first()
        assert new_mv.title == "Кино"
        assert new_mv.description == "Описание"
        assert str(new_mv.movie_running_time) == "1:30:00"
        directors_list_id = list(new_mv.directors.values_list('id', flat=True))
        genres_list_id = list(new_mv.genres.values_list('id', flat=True))
        assert directors_list_id == directors
        assert genres_list_id == genres

    def test_delete(self):
        movies = baker.make("Movie",10)
        r = self.client.get('/api/movies/')
        data = r.json()
        assert len(data) == 10
        movie_id_to_delete = movies[3].id
        self.client.delete(f'/api/movies/{movie_id_to_delete}/')
        r = self.client.get('/api/movies/')
        data = r.json()
        assert len(data) == 9
        assert movie_id_to_delete not in [i['id'] for i in data]

    def test_update(self):
        movies = baker.make("Movie", 10)
        movie: Movie = movies[2]
        r = self.client.get(f'/api/movies/{movie.id}/')
        data = r.json()
        assert data['title'] == movie.title
        r = self.client.patch(f'/api/movies/{movie.id}/',{
            'title': 'Кино'
        })
        assert r.status_code == 200
        r = self.client.get(f'/api/movies/{movie.id}/')
        data = r.json()
        assert data['title'] == "Кино"
        movie.refresh_from_db()
        assert data['title'] == movie.title

class MovieHallsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_get_list(self):
        movie_hall = baker.make("movies.MovieHall")
        r = self.client.get('/api/halls/')
        data = r.json()
        print(data)
        assert movie_hall.id == data[0]['id']
        assert movie_hall.is_imax == data[0]['is_imax']
        assert movie_hall.count_of_seats == data[0]['count_of_seats']

    def test_create(self):
        r = self.client.post("/api/halls/",{
            'sequence_number': 1,
            'count_of_seats': 56
        })
        new_mv_hl_id = r.json()['id']
        mv_hls = MovieHall.objects.all()
        assert len(mv_hls) == 1
        new_mv_hl = MovieHall.objects.filter(id = new_mv_hl_id).first()
        assert new_mv_hl.sequence_number == 1
        assert new_mv_hl.count_of_seats == 56
        assert new_mv_hl.is_imax == False

    def test_delete(self):
        movie_halls = baker.make("MovieHall",10)
        r = self.client.get('/api/halls/')
        data = r.json()
        assert len(data) == 10
        movie_hall_id_to_delete = movie_halls[3].id
        self.client.delete(f'/api/halls/{movie_hall_id_to_delete}/')
        r = self.client.get('/api/halls/')
        data = r.json()
        assert len(data) == 9
        assert movie_hall_id_to_delete not in [i['id'] for i in data]

    def test_update(self):
        movie_halls = baker.make("MovieHall", 10)
        movie_hall: MovieHall = movie_halls[2]
        r = self.client.get(f'/api/halls/{movie_hall.id}/')
        data = r.json()
        assert data['count_of_seats'] == movie_hall.count_of_seats
        r = self.client.patch(f'/api/halls/{movie_hall.id}/',{
            'count_of_seats': 450
        })
        assert r.status_code == 200
        r = self.client.get(f'/api/halls/{movie_hall.id}/')
        data = r.json()
        assert data['count_of_seats'] == 450
        movie_hall.refresh_from_db()
        assert data['count_of_seats'] == movie_hall.count_of_seats

class MovieSessionsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        mv_hl = baker.make("movies.MovieHall")
        mv = baker.make("Movie")
        movie_session = baker.make("movies.MovieSession", movie_hall = mv_hl, movie = mv, date_of_event = '2025-12-15T19:34:04.489323Z')
        r = self.client.get('/api/sessions/')
        data = r.json()
        print(data)
        assert movie_session.id == data[0]['id']
        assert movie_session.movie_hall.id == data[0]['movie_hall']
        assert movie_session.movie.id == data[0]['movie']
        assert str(movie_session.date_of_event) == data[0]['date_of_event']

    def test_create(self):
        mv_hl = baker.make("MovieHall")
        mv = baker.make("Movie")
        r = self.client.post("/api/sessions/",{
            'movie_hall': mv_hl.id,
            'movie': mv.id,
            'date_of_event': datetime.datetime(2025,12,15,22,30)
        })
        new_mv_session_id = r.json()['id']
        mv_sessions = MovieSession.objects.all()
        assert len(mv_sessions) == 1
        new_mv_session = MovieSession.objects.filter(id = new_mv_session_id).first()
        assert new_mv_session.movie_hall == mv_hl
        assert new_mv_session.movie == mv
        new_mv_session_date_of_event = new_mv_session.date_of_event.strftime("%m/%d/%Y, %H:%M:%S")
        input_date_of_event = datetime.datetime(2025,12,15,22,30).strftime("%m/%d/%Y, %H:%M:%S")
        assert new_mv_session_date_of_event == input_date_of_event

    def test_delete(self):
        movie_sessions = baker.make("MovieSession",10)
        r = self.client.get('/api/sessions/')
        data = r.json()
        assert len(data) == 10
        movie_session_id_to_delete = movie_sessions[3].id
        self.client.delete(f'/api/sessions/{movie_session_id_to_delete}/')
        r = self.client.get('/api/sessions/')
        data = r.json()
        assert len(data) == 9
        assert movie_session_id_to_delete not in [i['id'] for i in data]

    def test_update(self):
        movie = baker.make('Movie', id = 1256)
        movie_sessions = baker.make("MovieSession", 10)
        movie_session: MovieSession = movie_sessions[2]
        r = self.client.get(f'/api/sessions/{movie_session.id}/')
        data = r.json()
        assert data['movie'] == movie_session.movie
        r = self.client.patch(f'/api/sessions/{movie_session.id}/',{
            'movie': movie.id
        })
        assert r.status_code == 200
        r = self.client.get(f'/api/sessions/{movie_session.id}/')
        data = r.json()
        assert data['movie'] == movie.id
        movie_session.refresh_from_db()
        assert data['movie'] == movie_session.movie.id

class TicketsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        m_s = baker.make("movies.MovieSession")
        ticket = baker.make("movies.Ticket", movie_session = m_s)
        r = self.client.get('/api/tickets/')
        data = r.json()
        print(data)
        assert ticket.id == data[0]['id']
        assert ticket.movie_session.id == data[0]['movie_session']
        assert ticket.count_of_seats_purchased == data[0]['count_of_seats_purchased']

    def test_create(self):
        mv_session = baker.make('MovieSession')
        r = self.client.post("/api/tickets/",{
            'movie_session': mv_session.id,
            'count_of_seats_purchased': 450
        })
        new_tckt_id = r.json()['id']
        mv_tckts = Ticket.objects.all()
        assert len(mv_tckts) == 1
        new_tckt = Ticket.objects.filter(id = new_tckt_id).first()
        assert new_tckt.movie_session == mv_session
        assert new_tckt.count_of_seats_purchased == 450

    def test_delete(self):
        tickets = baker.make("Ticket",10)
        r = self.client.get('/api/tickets/')
        data = r.json()
        assert len(data) == 10
        ticket_id_to_delete = tickets[3].id
        self.client.delete(f'/api/tickets/{ticket_id_to_delete}/')
        r = self.client.get('/api/tickets/')
        data = r.json()
        assert len(data) == 9
        assert ticket_id_to_delete not in [i['id'] for i in data] 
        
    def test_update(self):
        tickets = baker.make("Ticket", 10)
        ticket: Ticket = tickets[2]
        r = self.client.get(f'/api/tickets/{ticket.id}/')
        data = r.json()
        assert data['count_of_seats_purchased'] == ticket.count_of_seats_purchased
        r = self.client.patch(f'/api/tickets/{ticket.id}/',{
            'count_of_seats_purchased': 3
        })
        assert r.status_code == 200
        r = self.client.get(f'/api/tickets/{ticket.id}/')
        data = r.json()
        assert data['count_of_seats_purchased'] == 3
        ticket.refresh_from_db()
        assert data['count_of_seats_purchased'] == ticket.count_of_seats_purchased