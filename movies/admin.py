from django.contrib import admin
from .models import Movie, Genre, Score, Actor
# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'audience', 'poster_url', 'description', 'director')
    

class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class ActorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

    
admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Score)
admin.site.register(Actor)