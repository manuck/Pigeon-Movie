from django.shortcuts import render, redirect, get_object_or-
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Movie, Actor, Genre, Score
from .forms import ScoreForm,
from django.db.models import Avg
# Create your views here.
def index(request):
    movies = Movie.objects.all().annotate(score_avg=Avg('score__value'))
    return render(request, 'index.html', {'movies':movies})
    
    
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    form = ScoreForm()
    context = {'movie': movie, 'form': form}
    return render(request, 'detail.html', context)

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