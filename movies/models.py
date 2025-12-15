from django.db import models
from datetime import date, time
import datetime
class Genre(models.Model):
    title = models.TextField("Название")
    description = models.TextField("Описание", null = True)
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
    def __str__(self) -> str:
        return self.title
class Director(models.Model):
    full_name = models.TextField("Полное имя")
    date_of_birth  = models.DateField("Дата рождения")
    class Meta:
        verbose_name = "Режиссер"
        verbose_name_plural = "Режиссеры"
    def __str__(self) -> str:
        return self.full_name
class Movie(models.Model):
    title = models.TextField("Название")
    description = models.TextField("Описание фильма")
    movie_running_time = models.DurationField("Хронометраж фильма")
    directors = models.ManyToManyField('Director', related_name='movies_directors',verbose_name="Режиссеры")
    genres = models.ManyToManyField('Genre', related_name='movies_genres',verbose_name="Жанры")
    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
    def __str__(self) -> str:
        return self.title
class MovieHall(models.Model):
    sequence_number = models.PositiveIntegerField("Порядковый номер зала")
    is_imax = models.BooleanField("IMAX", default = False)
    count_of_seats = models.PositiveIntegerField("Количество мест")
    class Meta:
        verbose_name = "Кинозал"
        verbose_name_plural = "Кинозалы"
class MovieSession(models.Model):
    movie_hall = models.ForeignKey('MovieHall', on_delete = models.CASCADE,verbose_name='Зал', null = True)
    movie = models.ForeignKey('Movie', on_delete = models.CASCADE,verbose_name='Фильм', null = True)
    date_of_event = models.DateTimeField("Дата и время проведения")
    class Meta:
        verbose_name = "Киносеанс"
        verbose_name_plural = "Киносеансы"
class Ticket(models.Model):
    movie_session = models.ForeignKey('MovieSession', on_delete = models.CASCADE,verbose_name='Сеанс', null = True)
    count_of_seats_purchased = models.PositiveIntegerField("Цена")
    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"