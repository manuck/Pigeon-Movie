from django.urls import path
from . import views

app_name = "movies"
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:genre_pk>/genre', views.genre, name='genre'),
    path('mylist/', views.mylist, name='mylist'),
    path('adult/', views.adult, name='adult'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('new/', views.new, name='new'),
    path('<int:movie_pk>/edit', views.edit, name='edit'),
    path('delete/<int:movie_pk>/', views.delete, name='delete'),
    path('<int:movie_pk>/scores', views.score_create, name='score_create'),
    path('<int:movie_pk>/scores/<int:score_pk>/delete/', views.score_delete, name='score_delete'),
    path('search/',views.search, name="search"),
    path('donate/',views.donate,name="donate"),
]