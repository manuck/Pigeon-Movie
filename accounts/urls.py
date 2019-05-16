from django.urls import path
from . import views

app_name= "accounts"
urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('delete/',views.delete,name="delete"),
    path('update/',views.update,name="update"),
    path('password/',views.password,name="password"),
    path('userlist/',views.userlist,name="userlist"),
    path('<int:user_pk>/',views.user_detail,name="user_detail"),  
]