from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
    
class Genre(models.Model):
    name = models.CharField(max_length=150)
    
    def __str__(self):
        return f'{self.name}'
    
class Actor(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return f'{self.name}'
        
class Movie(models.Model):
    title = models.CharField(max_length=150)
    audience = models.IntegerField()
    view_age = models.IntegerField()
    poster_url = models.TextField()
    trailer = models.TextField()
    description = models.TextField()
    director = models.CharField(max_length=45)
    actors = models.ManyToManyField(Actor, blank=True, related_name='movie_actors')
    genres = models.ManyToManyField(Genre, blank=True, related_name='movie_genres')
    score_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        through = 'Score',
                                        related_name = 'score_movies'
                                        )
    # genre = models.ManyToManyField(...)
    


class Score(models.Model):
    content = models.CharField(max_length=30)
    value = models.IntegerField(validators=[MinValueValidator(1),
                                       MaxValueValidator(10)])
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)