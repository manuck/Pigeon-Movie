from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.decorators import login_required 
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import UserCreationForm, UserChangeForm
from django.views.decorators.http import require_http_methods, require_POST
from movies.models import Genre

# Create your views here.
def signup(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            gen = request.POST.getlist('gen')
            for i in gen:
                for j in Genre.objects.all():
                    if j.name == i:
                        user.favorite_genres.add(j.id)
            
            print(gen)
            print(user.username)
            print(user.date_of_birth)
            print(user.favorite_genres.name)
            # print(user.favorite_genres)
            auth_login(request, user)
            return redirect('movies:index')
    else:
        user_form = UserCreationForm()
    genres = Genre.objects.all()
    genre_list = [i for i in range(1,27)]
    # for i in genres:
    #     genre_list.append([i.id,i.name])
    print(genre_list)
    context = {'user_form':user_form,'genres':genres}
    return render(request,'accounts/signup.html',context)
    

def login(request):
    if request.method == "POST":
        if request.user.is_authenticated:
        	return redirect('movies:index')
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect('movies:index')
    else:
        login_form = AuthenticationForm()
    context = {'login_form':login_form}
    return render(request,'accounts/login.html',context)
    
    
@login_required
def logout(request):
    auth_logout(request)
    return redirect('movies:index')

# 회원 탈퇴
@login_required
def delete(request):
    request.user.delete()
    return redirect('movies:index')


@require_http_methods(["GET", "POST"])
@login_required
def update(request):
    if request.method == "POST":
        user_form = UserChangeForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user = user_form.save()
            gen = request.POST.getlist('gen')
            print(gen)
            
            for k in Genre.objects.all():
                user.favorite_genres.remove(k.id)
            for i in gen:
                for j in Genre.objects.all():
                    if j.name == i:
                        user.favorite_genres.add(j.id)
            auth_login(request, user)       
            return redirect('movies:index')
    else:
        user_form = UserChangeForm(instance=request.user)
    genres = Genre.objects.all()
    geng = request.user.favorite_genres.all()
    print(geng)
    for i in geng:
        print(i.name)
    
    
    
    context = {'user_form':user_form,'genres':genres,'geng':geng}
    return render(request,'accounts/update.html',context)

@require_http_methods(["GET", "POST"])
@login_required
def password(request):
    if request.method == "POST":
        user_form = PasswordChangeForm(request.user, request.POST)
        if user_form.is_valid():
            user = user_form.save()
            update_session_auth_hash(request, user)
            return redirect('movies:index')
    else:
        user_form = PasswordChangeForm(request.user)
    context  = {'user_form':user_form}
    return render(request, 'accounts/update.html',context)
    
@login_required
def userlist(request):
    if not request.user.is_admin:
        return redirect('movies:index')
    User = get_user_model()
    users = User.objects.all()
    return render(request,'accounts/userlist.html',{'users':users})

@login_required
def user_detail(request,user_pk):
    if not request.user.is_admin:
        return redirect('movies:index')
    User = get_user_model()
    user = get_object_or_404(User,pk=user_pk)
    context = {'user_detail':user}
    return render(request,'accounts/userdetail.html',context)