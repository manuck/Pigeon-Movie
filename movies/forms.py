from django import forms
from .models import Score, Movie, Genre
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ScoreForm(forms.ModelForm):
    content = forms.CharField(max_length=30,label="내용",widget=forms.Textarea(attrs = {'cols': '40', 'rows': '1','class':'noresize'}))
    value = forms.IntegerField(min_value=1,max_value=10,label="평점")
    
    class Meta:
        model = Score
        labels = {'content': '내용', 'value':'평점'}
        fields = ['content', 'value']
        

class MovieForm(forms.ModelForm) :
    class Meta :
        model = Movie
        labels={'title' : '제목', 'audience' : '관객 수', 'view_age':'등급' ,'poster_url' : '이미지링크','director':'감독' ,'description':'설명', 'genres' : '장르 선택', 'actors':'배우', 'trailer':'예고편'}
        fields = ['title','audience','view_age','poster_url', 'trailer', 'director','description','genres', 'actors']

# class GenreForm(forms.ModelForm):
#     class Meta:
#         model = Genre
#         fields = ['name']