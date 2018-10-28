from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path('new/', views.create, name='create'),
    path('login/', views.logIn, name='login'),
    path('logout/', views.logOut, name='logout')
]
