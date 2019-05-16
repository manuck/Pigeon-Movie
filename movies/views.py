from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from movies.models import Movie, Actor, Genre, Score
from .forms import ScoreForm, MovieForm
from django.db.models import Avg
import datetime
# Create your views here.

@login_required
def index(request):
    movie_list = Movie.objects.all().annotate(score_avg=Avg('score__value'))
    page = request.GET.get('page', 1)
    paginator = Paginator(movie_list, 8)
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    genre_list = Genre.objects.all()
    user = request.user
    usergenres = user.favorite_genres.all()
    user_age = datetime.datetime.today().year - user.date_of_birth.year
    genres = []
    for i in genre_list:
        if i.name == '에로':
            if user_age > 18:
                genres.append(i)
            else:
                pass
        else:
            genres.append(i)
            
    return render(request, 'index.html', {'movies':movies, 'user_age':user_age, 'genres':genres})

@login_required
def mylist(request):
    movie_list = Movie.objects.all().annotate(score_avg=Avg('score__value'))
    genre_list = Genre.objects.all()
    user = request.user
    usergenres = user.favorite_genres.all()
    like = []
    for movie in movie_list:
        for usergenre in usergenres:
            a = 0
            for mvgenre in movie.genres.all():
                if usergenre.id == mvgenre.id:
                    like.append(movie)
                    a=1   
                    break
            if a==1:
                break
    page = request.GET.get('page', 1)
    paginator = Paginator(like, 8)
    try:
        like = paginator.page(page)
    except PageNotAnInteger:
        like = paginator.page(1)
    except EmptyPage:
        like = paginator.page(paginator.num_pages)
    print(like)
    print(usergenres)
    user_age = datetime.datetime.today().year - user.date_of_birth.year
    genres = []
    for i in genre_list:
        if i.name == '에로':
            if user_age > 18:
                genres.append(i)
            else:
                pass
        else:
            genres.append(i)
    return render(request, 'mylist.html', {'user_age':user_age, 'like':like, 'genres':genres,'usergenres':usergenres})

@login_required
def genre(request, genre_pk):
    movies = Movie.objects.all().annotate(score_avg=Avg('score__value'))
    genre_list = Genre.objects.all()
    user = request.user
    usergenres = user.favorite_genres.all()
    
    genreMovies = []
    for movie in movies:
        for mvgenre in movie.genres.all():
            if genre_pk == mvgenre.id:
                genreMovies.append(movie)  
                break
    print(genreMovies)
    page = request.GET.get('page', 1)
    paginator = Paginator(genreMovies, 8)
    try:
        genreMovies = paginator.page(page)
    except PageNotAnInteger:
        genreMovies = paginator.page(1)
    except EmptyPage:
        genreMovies = paginator.page(paginator.num_pages)
    user_age = datetime.datetime.today().year - user.date_of_birth.year
    genres = []
    genrename=''
    for i in genre_list:
        if i.name == '에로':
            if user_age > 18:
                genres.append(i)
            else:
                pass
        else:
            genres.append(i)
        if i.pk == genre_pk:
            genrename = i.name
    return render(request, 'genre_movie.html', {'movies':movies, 'user_age':user_age, 'genreMovies':genreMovies, 'genres':genres, 'genrename':genrename})

@login_required
def adult(request):
    movies = Movie.objects.all().annotate(score_avg=Avg('score__value'))
    user = request.user
    user_age = datetime.datetime.today().year - user.date_of_birth.year
    if user_age > 18:
        return render(request, 'adult.html', {'movies':movies, 'user_age':user_age}) 
    else:
        return redirect('movies:index')
    
@login_required   
def detail(request, movie_pk):
    movie = Movie.objects.annotate(score_avg=Avg('score__value')).get(pk=movie_pk)
    actors = movie.actors.all()
    genres = movie.genres.all()
    allgenre = Genre.objects.all()
    scores = movie.score_set.all()
    score_form = ScoreForm()
    user = request.user
    user_age = datetime.datetime.today().year - user.date_of_birth.year
    context = {
        'movie':movie,
        'scores':scores,
        'actors':actors,
        'genres':genres,
        'score_form':score_form,
        'allgenre':allgenre
        }
    if user_age > movie.view_age:
        return render(request, 'detail.html', context)
    else:
        return redirect('movies:index')

@login_required
def new(request) :
    if request.user.is_admin:
        if request.method == "POST" :
            movie_form=MovieForm(request.POST)
            if movie_form.is_valid() :
                movie=movie_form.save()
                return redirect('movies:index')
        else :
            movie_form=MovieForm()
        context={'movie_form':movie_form}
        return render(request,'form.html',context)
    else:
        return redirect('movies:index')

@login_required
def edit(request, movie_pk):
    movie = get_object_or_404(Movie,pk=movie_pk)
    if request.method == "POST" :
        movie_form = MovieForm(request.POST, instance=movie)
        if movie_form.is_valid() :
            movie = movie_form.save()
            return redirect('movies:detail', movie.pk)
    else :
        movie_form=MovieForm(instance=movie)
    context = {'movie_form' : movie_form}
    return render(request,'form.html',context)

@login_required
def delete(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    movie.delete()
    return redirect('movies:index')

@require_POST
@login_required
def score_create(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    if request.user.is_authenticated:
        if request.method == 'POST':
            score_form = ScoreForm(request.POST)
            if score_form.is_valid():
                score = score_form.save(commit=False)
                score.movie = movie
                score.user = request.user
                score.save()
                return redirect('movies:detail', movie.pk)
        else:
            score_form = ScoreForm()
        context = {'movie': movie, 'score_form': score_form}
        return render(request, 'detail.html', context)

def score_delete(request, movie_pk, score_pk):
    if request.method == "POST":
        score = Score.objects.get(pk=score_pk)
        score.delete()
    return redirect('movies:detail', movie_pk)

def search(request):
    title = request.GET.get('title')
    movie_list = Movie.objects.filter(title__contains=title)
    user = request.user
    user_age = datetime.datetime.today().year - user.date_of_birth.year
    genre_list = Genre.objects.all()
    genres = []
    for j in genre_list:
        if j.name == '에로':
            if user_age > 18:
                genres.append(j)
            else:
                pass
        else:
            genres.append(j)
    movies = []
    for i in movie_list:
        if i.view_age < user_age:
            print(i)
            movies.append(i)
    context = {
        'movies':movies,
        'genres':genres,
        'user_age':user_age
        }
    return render(request, 'index.html', context)
    
def donate(request):
    return render(request,'donate.html')